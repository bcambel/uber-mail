import logging
import time
from datetime import datetime
import json
from app import startup, db, settings
from mailing import Postman
from models import Email, Statuses


class MailService(object):
    """
    1. Query the Database.
    2. Fetch a single item.
    3. Mark that item in_progress
    4. Once sent, set item free either finished/queued to be retried soon
    """
    def __init__(self, db):
        self.postman = Postman(**{'mailgun_key': settings.get('default', 'mailgun_key'),
                                  'mailgun_domain': settings.get("default", "mailgun_domain"),
                                  'sendgrid_key': settings.get('default', 'sendgrid_key')})
        self.db = db

    def lock_instance(self, mail):

        mail.status = Statuses.inprogress
        mail.lock_at = datetime.utcnow()
        self.db.session.add(mail)
        self.db.session.commit()

    def release_instance(self, mail, status=Statuses.success, result=None):

        mail.status = status
        mail.lock = None
        mail.updated_at = datetime.utcnow()
        mail.result = json.dumps(result) if result is not None else None

        self.db.session.add(mail)
        self.db.session.commit()

    def send_mail(self, mail):
        # handle timeouts. what if the service does not return a response in X seconds/minutes ?
        delivery_result = self.postman.deliver(mail.from_address, mail.to_address, mail.subject, mail.mail)

        logging.info(mail.id, delivery_result)
        status_code = delivery_result['status']

        if status_code >= 429:  # classic 5xx + 429 (Too many requests)
            self.postman.switch()
            self.release_instance(mail, status=Statuses.queued)
        elif delivery_result['success']:
            self.release_instance(mail, Statuses.success, delivery_result)
        else:
            # handle 3xx and 4xx errors.
            self.release_instance(mail, Statuses.error, delivery_result)

    def query(self):
        logging.info("Query Mail Queue")
        eq = Email.query.filter(Email.status == Statuses.queued)

        for mail in eq:
            self.lock_instance(mail)
            self.send_mail(mail)
            break

    def forever(self):
        while True:
            self.query()
            time.sleep(10)


if __name__ == "__main__":
    ms = MailService()
    ms.forever()
