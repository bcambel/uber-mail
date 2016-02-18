from nose import with_setup
from nose.tools import nottest
import uuid
from app import *
from mail_service import MailService
from models import Email, Statuses


def new_email():
    m = Email()
    m.id = str(uuid.uuid4())
    m.status = Statuses.queued
    m.from_address = 'from'
    m.to_address = 'from'
    m.subject = 'test'
    m.mail = 'test'
    return m


def test_successfull_mail():

    m = new_email()

    ms = MailService(db)

    class MockPostman(object):

        def deliver(self, from_email, to, subject, text, html=None):
            return {'success': True, 'status': 200}

    ms.postman = MockPostman()

    ms.send_mail(m)

    mail = Email.by_id(str(m.id))

    assert mail.status == Statuses.success


def test_mail_service_failover():
    m = new_email()

    ms = MailService(db)

    class MockPostman(object):
        def __init__(self):
            self.switched = False

        def deliver(self, from_email, to, subject, text, html=None):
            return {'success': False, 'status': 500}

        def switch(self):
            self.switched = True

    ms.postman = MockPostman()

    ms.send_mail(m)

    mail = Email.by_id(str(m.id))

    assert ms.postman.switched

def test_mail_service_error_should_set_status():
    m = new_email()

    ms = MailService(db)

    class MockPostman(object):
        def deliver(self, from_email, to, subject, text, html=None):
            return {'success': False, 'status': 400}

    ms.postman = MockPostman()

    ms.send_mail(m)

    mail = Email.by_id(str(m.id))

    assert mail.status == Statuses.error