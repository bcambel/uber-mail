from nose import with_setup
from nose.tools import nottest
from app import *
from mailing import Postman, MailGunPostman, SendGridPostman

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