# Mail Service

A REST based Mail service that sends emails.

Default services uses Mailgun, failover service is Sendgrid.

Mail Service composed of ;

- Flask
- Flask Restful
- Flask Restful Swagger (API Documentation)
- Flask Admin
- Sentry (Error reporting)

components and behind the scenes uses SQLAlchemy to store the incoming mail requests into the database. A separate process (Mail Service) polls the database and tries to send email to the 3rd parties.

### Experience

- Python (experienced 2+ years)
- Flask (somewhat experienced)
- Postgres (experienced)

The last 1.5+ years, I haven't been active on Python that much, there might be some missing bits and pieces, not doing things in the Pythonic way.

I kept the application side as simple as possible. No HTML page, API only.

## Installation

```bash
virtualenv venv
source venv/bin/active
pip install -r requirements.txt
```

uber-mail requires postgres installed on a machine

```bash
sudo su postgres
psql < scripts/db.sql
```
will create a database, a user, and create the necessary table(s). Adding superuser rights to this user is **not recommended** for production environments.

## Development

Make sure you have installed

```bash
# ubuntu
sudo apt-get install -y build-essential python-dev libffi-dev libssl-dev libgdbm-dev libpq-dev
```

Copy ```settings.cfg.sample``` to ```settings.cfg``` and fill in the required arguments.

```bash
cp settings.cfg.sample settings.cfg
```

In a development environment, once the virtual env is activated, start the API Service

```bash
python app.py --config settings.cfg
```
in a separate terminal window start the mail service

 ```bash
python mail_service.py
 ```

## Tests

In your terminal run ```nosetests``` to run all the tests, to see if 20+ tests all running correctly.


# Usage

Either go to [http://localhost:5000/admin/email](http://localhost:5000/admin/email) to create a new email or do a HTTP POST to the service. If you create a new mail object, set the status of the object 'queued' or leave blank.

```bash
# if you have HTTPIE installed
http POST localhost:5000/mail from="bcambel@gmail.com" to="bcambel@gmail.com" subject="Hello" text="This email will be sent via a Mail gateway" --form
# if not fall back to cURL
curl --data "from=bcambel@gmail.com&to=bcambel@gmail.com&subject=Hello&text=This email will be sent via a Mail gateway" localhost:5000/mail
```

## Production

```Config``` folder contains nginx and supervisor configuration samples. It's recommended to use these at least. One addition would be to use **uwsgi** or **gunicorn** or similar.

There would be 2 supervised processed running ```ubermail``` and ```ubermail_service``` that could be managed by the ```supervisorctl``` command.

All application log output will be redirected to ```syslog``` automatically via supervisor's ```stdout_log``` directive set to ```syslog```. From there on, you may use a service like [https://papertrailapp.com/](https://papertrailapp.com/) to manage your logs.

## Architecture

![mail_service](https://cloud.githubusercontent.com/assets/144385/13109081/73411c14-d577-11e5-891b-bd66c277823b.png)

Each mail post request stored into DB and queued for sending in some later time. API clients can record the email id, and query the API anytime to retrieve the status of the email sending operation. Each email contains a result field which stores the response of the API gateway. In SendGrid case, the result message contains the internal SendGrid ID.

### Rationale

Storing incoming mail requests into DB has the following benefits.

1. A request will be safe. It is stored into a transactional db. It is there. Not like MongoDB there, it is actually safely stored into disk.
2. If necessary, additional logic like cancel, retry, scheduling could be easily added.
3. Restart proof. It doesn't matter if the front-end server is restarted or not.
4. Horizontally scalable components. Add more API servers, add more mail service.
5. Multiple services; API Service and Mail Service. Stop mail service, upgrade code, API service will be still operational.
6. Add more Email providers to increase overall service output. (More active email gateways)
7. A flood in incoming mail requests will not affect the overall output of the system, as long as the DB is available.


## Enhancements

- Current approach to switch between providers with a single 5xx exception is simple but naive.
- Mail service sends email one by one. (introduce Multiprocessing.Pool to send multiple emails at the same time)
- Adding more mail service might introduce locking same email to dequeue. A better approach is necessary.
- After an email marked as inprogress, a separate check should be made to figure if send operations is still in progress.
- State machines are prone to dead-locks.
- Application does not take into account restarts. If restarted, the default service is still Mailgun. No state is saved.
- A more advanced approach should be designed to decide based on a consequent number of fails. Each service will fail eventually at some point of time. The crucial thing is to realize a complete service meltdown.
- What if we try to send millions of emails ?
- Current DB interaction is also naive. Db will also fail. More exception handling.
- Result field of the Mail object could be a field of ```JSON``` in Postgres rather than a ```text``` field so that we can query JSON directly thanks to awesomeness of Postgres.

## Endpoints

Navigate to [http://localhost:5000/api/spec](http://localhost:5000/api/spec) to see all the available API endpoints, their required parameters and basic descriptions.

Mail service accepts a POST request with the following parameters;

### POST ```/mail```

```json
{"from": "bcambel@gmail.com",
  "to": "bcambel@gmail.com",
  "subject": "Hello",
  "text": "Is this yours bahadir?",
  "html": "Is this yours bahadir?"}
```

and returns

```json
{
    "created_at": "2016-02-17 09:38:55.581043",
    "from_address": "bcambel@gmail.com",
    "id": "be7f79dd-79f3-43bb-8f49-e60cd7ac2d89",
    "mail": "Is this yours bahadir?",
    "result": "None",
    "status": "queued",
    "subject": "Hello",
    "success": true,
    "to_address": "bcambel@gmail.com",
    "updated_at": "2016-02-17 09:38:55.581055"
}

```

### GET ```/mail/<id>```

Mail service accepts an ID parameter and returns the mail object.


```json
{
    "created_at": "2016-02-17 09:38:55.581043",
    "from_address": "bcambel@gmail.com",
    "id": "be7f79dd-79f3-43bb-8f49-e60cd7ac2d89",
    "mail": "Is this yours bahadir?",
    "result": "None",
    "status": "queued",
    "subject": "Hello",
    "success": true,
    "to_address": "bcambel@gmail.com",
    "updated_at": "2016-02-17 09:38:55.581055"
}

```

### GET ```/admin```

Flask Admin application to manage mail objects. Theorically only accessible by the administrator of the application. For demostration purposes, admin app is open to everyone.

## Todo

[] Delete email object after tests complete ( on tear down )
[] Handle Mail gateway timeouts
[+] Handle 429(Too many requests) by Sendgrid

