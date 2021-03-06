from flanker.addresslib import address
from flask import request
from flask_restful import Resource, abort
from flask_restful_swagger import swagger
import logging
import json

from models import Email

email_fields = ['from', 'to']
required_fields = ['from', 'to', 'subject', 'text']


def validate_form(form):
    messages = []

    for field in required_fields:
        if field not in form or len(form.get(field, "")) <= 0:
            messages.append({'field': field,
                             'message': "Missing required field '{}'".format(field)})

    for field in email_fields:
        if field in form:
            email_address = form[field]
            failed_emails = None

            if "," in email_address:
                parsed_email, failed_emails = address.parse_list(email_address, as_tuple=True)
            else:
                parsed_email = address.parse(email_address)

            if parsed_email is None:
                messages.append({'field': field,
                                 'message': "Email field '{}' is not a valid email address {}".format(field, form[field])})
            if failed_emails is not None and len(failed_emails) > 0:
                messages.append({'field': field,
                                 'message': "Email field '{}' contains invalid email address(es)".format(field),
                                 'parsed': ",".join([str(e) for e in parsed_email] or ""),
                                 'unparsed': ",".join([str(e) for e in failed_emails])})

    return messages


class EmailResource(Resource):
    @swagger.operation(notes='Retrieve email status by /mail/<id>',
                       responseClass=Email.__name__,
                       nickname='fetch email',
                       parameters=[{'name': 'id', 'dataType': 'string'}],
                       response_messages=[{'code': 200, 'message': 'An email with given ID is found and returned'},
                                          {'code': 404, 'message': 'Email not found error'}])
    def get(self, id):
        email = Email.by_id(id)

        if email is None:
                abort(404, message="Mail not found")

        return email.as_dict()

class SendEmailResource(Resource):
    @swagger.operation(notes='Submit an email to send',
                       responseClass=Email.__name__,
                       nickname='submit a new email',
                       parameters=[{'name': 'from', "required": True, "dataType": 'string'},
                                   {"required": True, 'name': 'to', "dataType": 'string', 'description': 'A full email validation done. Supply a comma separated email addresses to send the email to multiple destinations'},
                                   {"required": True, 'name': 'subject', "dataType": 'string'},
                                   {"required": True, 'name': 'text', "dataType": 'string'}],
                       response_messages=[{'code': 200, 'message': 'An email created and added to the queueu'},
                                          {'code': 400, 'message': 'Invalid Parameters'}])
    def post(self, id=None):

        data = request.form

        validation_messages = validate_form(data)

        if len(validation_messages) > 0:
            abort(400, message=validation_messages)

        logging.info(data)

        email_id = Email.insert(data)

        logging.info("Commit completed " + email_id)

        mail = Email.by_id(email_id).as_dict()
        mail.update({'success': True})

        return mail
