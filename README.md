# Mail Service

A REST based Mail service that sends emails.

Default services uses Mailgun, failover service is Sendgrid.

Mail Service composed of ;

- Flask
- Flask Restful
- Flask Admin

components and behind the scenes uses SQLAlchemy to store the incoming mail requests into the database. A separate process polls the database
and tries to send email to the parties.

## Endpoints

Mail service accepts a POST request with the following parameters;

### /mail

```json
{"from": "bcambel@gmail.com",
  "to": "bcambel@gmail.com",
  "subject": 'Hello',
  "text": 'Is this yours bahadir?',
  "html": 'Is this yours bahadir?'}
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

### ```/mail/<id>```

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

### /admin

Flask Admin application to manage mail objects. Theorically only accessible by the administrator of the application. For demostration purposes, admin app is open to everyone.

## Todo

[] Delete email object after tests complete ( on tear down )
[] Handle Mail gateway timeouts
[+] Handle 429(Too many requests) by Sendgrid