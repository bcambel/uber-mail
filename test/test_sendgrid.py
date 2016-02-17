from nose import with_setup
from nose.tools import nottest
from app import *
from mailing import Postman
from test_base import match_result

postman = Postman(**{ 'mailgun_key' : settings.get('default', 'mailgun_key'),
                  'mailgun_domain': settings.get("default", "mailgun_domain"),
                  'sendgrid_key' : settings.get('default' ,'sendgrid_key')})

def test_invalid_from_field():
  a = postman.sendgrid.deliver("", "bcambel@gmail.com", "Delivery of your good", "Hey Bahadir, delivery will be late")

  expected_result = {'status': 400,
                     'result': {u'message': u'error', u'errors': [u'Empty from email address (required)']},
                     'success': False}
  print a
  match_result(a, expected_result)

@nottest
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
  match_result(a, expected_result)


def setup_func():
  "Manipulate API key temporarily to cause the requests fail"
  postman.sendgrid.sg = sendgrid.SendGridClient(postman.sendgrid.api_key[::-1])

def teardown_func():
  "Rollback to the original(correct) key"
  postman.sendgrid.sg = sendgrid.SendGridClient(postman.sendgrid.api_key)

@with_setup(setup_func, teardown_func)
def test_invalid_api_key():
  """
  Sendgrid accepts empty To fields. Wow.
  Sendgrid accepts invalid email addresses.
  """

  a = postman.sendgrid.deliver("bcambel@gmail.com", "bcambel@gmail.com", "Delivery of your good", "Hey Bahadir, delivery will be late")

  print a
  assert a['status'] == 400

def test_send():
  a = postman.sendgrid.deliver("bcambel@gmail.com", "bcambel@gmail.com", "Delivery of your good", "Hey Bahadir, delivery will be late")
  print a

  match_result(a, {'status':200, 'result' : {'message':'success'}})

@nottest
def test_successfull_email_huge_text_request_returns_a_id():
  a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "Hello", "\n".join(100000 * ["Hey Bahadir, delivery will be late"]))

  print a
  assert a['status'] == 200 and "id" in a['result']