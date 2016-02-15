from flask import request
from flask_restful import Resource
import logging
from models import Email

class SendEmail(Resource):
  def get(self, id):
    email = Email.by_id(id)

    return email.as_dict()

  def post(self,id=None):

    data = request.form

    email_id = Email.insert(**data)
    logging.info("Commit completed " + email_id )

    mail = Email.by_id(email_id).as_dict()
    mail.update({'success':True})

    return mail