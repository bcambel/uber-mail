#tests.py
import nose
from nose.tools import nottest
from app import *
from mailing import Postman

postman = Postman(**{ 'mailgun_key' : settings.get('default', 'mailgun_key'),
                  'mailgun_domain': settings.get("default", "mailgun_domain"),
                  'sendgrid_key' : settings.get('default' ,'sendgrid_key')})

def test_invalid_from_field():
  a = postman.sendgrid.deliver("", "bcambel@gmail.com", "Delivery of your good", "Hey Bahadir, delivery will be late")

  excepted_result = {'status': 400,
                     'result': {u'message': u'error', u'errors': [u'Empty from email address (required)']},
                     'success': False}
  print a
  assert a == excepted_result

def test_invalid_to_field():
  """
  Sendgrid accepts empty To fields. Wow.
  Sendgrid accepts invalid email addresses.
  """
  a = postman.sendgrid.deliver("bcambel@.com", "", "Delivery of your good", "Hey Bahadir, delivery will be late")

  print a
  assert a['status'] == 200

def test_empty_text_field_fails():
  a = postman.sendgrid.deliver("bcambel@gmail.com", "bcambel@gmail.com", "", "")

  expected_result = {'status': 400,
                     'result': {u'message': u'error', u'errors': [u'Missing email body']},
                     'success': False}
  print a
  assert a == expected_result