from nose import with_setup
from nose.tools import nottest
import uuid
from app import *
from models import Email
from mailing import MailGunPostman, SendGridPostman
from mail_service import MailService
from test_base import init_postman

postman = init_postman()


def test_instances():
    assert type(postman.active) is MailGunPostman
    assert type(postman.alternate) is SendGridPostman

    postman.switch()

    assert type(postman.active) is SendGridPostman
    assert type(postman.alternate) is MailGunPostman

    postman.switch()

    assert type(postman.active) is MailGunPostman
    assert type(postman.alternate) is SendGridPostman
