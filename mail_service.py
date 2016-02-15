import logging
import time
from datetime import datetime
from app import startup, db, settings
from mailing import Postman
from models import Email

postman = Postman(**{ 'mailgun_key' : settings.get('default', 'mailgun_key'),
                  'mailgun_domain': settings.get("default", "mailgun_domain"),
                  'sendgrid_key' : settings.get('default' ,'sendgrid_key')})

# 1. Query the Database.
# 2. Fetch a single item.
# 3. Mark that item in_progress
# 4. Once sent, set item free either finished/queue to be retried soon

def lock_instance(mail):

  mail.status = 'inprogress'
  mail.lock_at = datetime.utcnow

  db.session.add(mail)
  db.session.commit()

def send_mail(mail):
  postman.deliver(mail.from_address, mail.to_address, mail.subject, mail.mail)


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