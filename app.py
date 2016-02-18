import argparse
from ConfigParser import RawConfigParser
from flask import Flask, request, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful_swagger import swagger
import logging
import os
from raven.contrib.flask import Sentry
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
flapp.config['SQLALCHEMY_DATABASE_URI'] = settings.get("default", "db")
flapp.secret_key = 'super secret key'
flapp.debug = True

sentry = Sentry(flapp,
                logging=True,
                level=logging.ERROR,
                dsn=settings.get("default", "sentry_dsn"))

# navigate to localhost:5000/admin to interact with Mail objects.
admin = Admin(flapp, name='MailServ', template_mode='bootstrap3')

api = swagger.docs(Api(flapp), apiVersion='1.0',
                   resourcePath='/',
                   produces=["application/json", "text/html"],
                   api_spec_url='/api/spec',
                   description='A Basic Mail Service API')

db = SQLAlchemy(flapp)

# app will crash on startup if can't connect
db.create_all()


def startup():
    from models import Email
    from rest import SendEmailResource, EmailResource
    admin.add_view(ModelView(Email, db.session))
    api.add_resource(SendEmailResource, '/mail')
    api.add_resource(EmailResource, '/mail/<string:id>')


@flapp.route("/error")
def error_demo():
    # demonstration of auto error capturing using Sentry.
    raise ValueError("Not a valid set.")

@flapp.route("/")
def home():
    return redirect("/api/spec")

if __name__ == "__main__":
    startup()
    flapp.run()
