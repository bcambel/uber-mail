from nose import with_setup
from nose.tools import nottest
import uuid
from app import *
from models import Email
from mailing import Postman, MailGunPostman, SendGridPostman
from mail_service import MailService

postman = Postman(**{ 'mailgun_key' : settings.get('default', 'mailgun_key'),
                  'mailgun_domain': settings.get("default", "mailgun_domain"),
                  'sendgrid_key' : settings.get('default' ,'sendgrid_key')})

def test_instances():
  assert type(postman.active) is MailGunPostman
  assert type(postman.alternate) is SendGridPostman

  postman.switch()

  assert type(postman.active) is SendGridPostman
  assert type(postman.alternate) is MailGunPostman

  postman.switch()

  assert type(postman.active) is MailGunPostman
  assert type(postman.alternate) is SendGridPostman

def new_email():
  m = Email()
  m.id = str(uuid.uuid4())
  m.status='queued'
  m.from_address='from'
  m.to_address='from'
  m.subject = 'test'
  m.mail='test'
  return m

def test_successfull_main():

  m = new_email()

  ms = MailService(db)

  class MockPostman(object):

    def deliver(self, from_email, to, subject, text, html=None):
      return {'success': True, 'status':200 }

  ms.postman = MockPostman()

  ms.send_mail(m)

  mail = Email.by_id(str(m.id))

  assert mail.status == "success"

def test_mail_service_failover():
  m = new_email()

  ms = MailService(db)

  class MockPostman(object):
    def __init__(self):
      self.switched = False

    def deliver(self, from_email, to, subject, text, html=None):
      return {'success': False, 'status': 500 }

    def switch(self):
      self.switched = True

  ms.postman = MockPostman()

  ms.send_mail(m)

  mail = Email.by_id(str(m.id))

  assert ms.postman.switched