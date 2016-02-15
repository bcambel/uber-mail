import argparse
from ConfigParser import RawConfigParser

from flask import Flask, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import logging
import os
import requests
import sendgrid


basedir = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(format='[%(asctime)s](%(filename)s#%(lineno)d)%(levelname)-7s %(message)s',
                    level=logging.NOTSET)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--config', default='settings.cfg')
args = parser.parse_args()

def read_config(config_file):
  cp = RawConfigParser()
  cp.read(config_file)
  return cp

settings = read_config(args.config)

flapp = Flask(__name__)
flapp.config['SQLALCHEMY_DATABASE_URI'] = settings.get("default","db")
flapp.secret_key = 'super secret key'
flapp.debug=True

# navigate to localhost:5000/admin to interact with Mail objects.
admin = Admin(flapp, name='MailServ', template_mode='bootstrap3')
api = Api(flapp)
db = SQLAlchemy(flapp)

db.create_all()

def startup():
  from models import Email
  from rest import SendEmail
  admin.add_view(ModelView(Email, db.session))
  api.add_resource(SendEmail,'/mail', '/mail/<string:id>')

@flapp.route("/")
def hello():
    pass


if __name__ == "__main__":
  startup()
  flapp.run()