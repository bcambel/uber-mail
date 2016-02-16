#tests.py
import nose
from nose.tools import nottest
from app import *
from mailing import Postman

postman = Postman(**{ 'mailgun_key' : settings.get('default', 'mailgun_key'),
                  'mailgun_domain': settings.get("default", "mailgun_domain"),
                  'sendgrid_key' : settings.get('default' ,'sendgrid_key')})

def test_invalid_from_field_fails():
  a = postman.mailgun.deliver("bcambel@.com", "bcambel@gmail.com", "Delivery of your good", "Hey Bahadir, delivery will be late")

  excepted_result = {'status': 400,
                     'result': {u'message': u"'from' parameter is not a valid address. please check documentation"},
                     'success': False}

  assert a == excepted_result

def test_empty_to_field_fails():
  a = postman.mailgun.deliver("bcambel@gmail.com", "", "Delivery of your good", "Hey Bahadir, delivery will be late")

  excepted_result = {'status': 400,
                     'result': {u'message': u"'to' parameter is not a valid address. please check documentation"},
                     'success': False}
  print a
  assert a == excepted_result

@nottest
def test_empty_subject_field_succeed():
  a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "", "Hey Bahadir, delivery will be late")

  assert a['status'] == 200

def test_empty_text_field_fails():
  a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "", "")

  expected_result = {'status': 400,
                     'result': {u'message': u"Need at least one of 'text' or 'html' parameters specified"},
                     'success': False}

  assert a == expected_result

def test_invalid_credentials_result_in_exception():
  postman.mailgun.api_key = postman.mailgun.api_key[::-1]
  a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "", "b")
  print a

  assert a['status'] == 401