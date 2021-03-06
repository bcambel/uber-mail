from nose import with_setup
from nose.tools import nottest
from app import *
from mailing import Postman
from test_base import match_result, init_postman

postman = init_postman()


def test_invalid_from_field_fails():
    a = postman.mailgun.deliver("bcambel@.com", "bcambel@gmail.com", "Delivery of your good", "Hey Bahadir, delivery will be late")

    expected_result = {'status': 400,
                       'result': {u'message': u"'from' parameter is not a valid address. please check documentation"},
                       'success': False}

    match_result(a, expected_result)


def test_empty_to_field_fails():
    a = postman.mailgun.deliver("bcambel@gmail.com", "", "Delivery of your good", "Hey Bahadir, delivery will be late")

    expected_result = {'status': 400,
                       'result': {u'message': u"'to' parameter is not a valid address. please check documentation"},
                       'success': False}
    print a
    match_result(a, expected_result)


def test_empty_subject_field_succeed():
    a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "", "Hey Bahadir, delivery will be late")

    assert a['status'] == 200


def test_empty_text_field_fails():
    a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "", "")

    expected_result = {'status': 400,
                       'result': {u'message': u"Need at least one of 'text' or 'html' parameters specified"},
                       'success': False}

    match_result(a, expected_result)


def setup_func():
    "Manipulate API key temporarily to cause the requests fail"
    postman.mailgun.api_key2, postman.mailgun.api_key = postman.mailgun.api_key, "invalid_key"


def teardown_func():
    "Rollback to the original(correct) key"
    postman.mailgun.api_key = postman.mailgun.api_key2


@with_setup(setup_func, teardown_func)
def test_invalid_credentials_result_in_exception():

    a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "", "b")
    print a
    assert a['status'] == 401


def test_successfull_email_request_returns_a_id():
    a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "Hello", "Hey Bahadir, delivery will be late")

    assert a['status'] == 200 and "id" in a['result']


@nottest
def test_successfull_email_huge_text_request_returns_a_id():
    a = postman.mailgun.deliver("bcambel@gmail.com", "bcambel@gmail.com", "Hello", "\n".join(100000 * ["Hey Bahadir, delivery will be late"]))

    print a
    assert a['status'] == 200 and "id" in a['result']
