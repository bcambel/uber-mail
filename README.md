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

```
from_address
to_address
subject
text
```

and returns

```
id
status
from_address
to_address
subject
text
```

### ```/mail/<id>```

Mail service accepts an ID parameter and returns the mail object.


```
id
status
from_address
to_address
subject
text
created_at
updated_at
```

### /admin

Flask Admin application to manage mail objects. Theorically only accessible by the administrator of the application. For demostration purposes, admin app is open to everyone.