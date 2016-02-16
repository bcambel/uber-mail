import logging
import time
from datetime import datetime
import json
from app import startup, db, settings
from mailing import Postman
from models import Email

postman = Postman(**{ 'mailgun_key' : settings.get('default', 'mailgun_key'),
                  'mailgun_domain': settings.get("default", "mailgun_domain"),
                  'sendgrid_key' : settings.get('default' ,'sendgrid_key')})

# 1. Query the Database.
# 2. Fetch a single item.
# 3. Mark that item in_progress
# 4. Once sent, set item free either finished/queued to be retried soon

def lock_instance(mail):

  mail.status = 'inprogress'
  mail.lock_at = datetime.utcnow()
  db.session.add(mail)
  db.session.commit()

def release_instance(mail, status='success', result=None):

  mail.status = status
  mail.lock = None
  mail.updated_at = datetime.utcnow()
  mail.result = result

  db.session.add(mail)
  db.session.commit()

def send_mail(mail):
  delivery_result = postman.deliver(mail.from_address, mail.to_address, mail.subject, mail.mail)

  logging.info(mail.id, delivery_result)

  if delivery_result['status'] >= 500:
    postman.switch()
    release_instance(mail, status='queued')
  elif delivery_result['success']:
    release_instance(mail, 'success', json.dumps(delivery_result))
  else:
    # handle 3xx and 4xx errors.
    release_instance(mail, 'error', json.dumps(delivery_result))

def query():
  logging.info("Query Mail Queue")
  eq = Email.query.filter(Email.status=='queued')

  for mail in eq:
    lock_instance(mail)
    send_mail(mail)
    break

def forever():
  while True:
    query()
    time.sleep(10)


if __name__ == "__main__":
  forever()