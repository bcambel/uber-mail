from app import settings
from mailing import Postman


def match_result(actual_result, expected_result):
    assert actual_result['status'] == expected_result['status'] and actual_result['result'] == expected_result['result']

postman = Postman(**{'mailgun_key': settings.get('default', 'mailgun_key'),
                      'mailgun_domain': settings.get("default", "mailgun_domain"),
                      'sendgrid_key': settings.get('default', 'sendgrid_key')})

def init_postman():
    return postman
