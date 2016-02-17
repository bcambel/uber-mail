import json
import logging
import requests

from app import *
from test_base import match_result

app_client = flapp.test_client()
startup()

base_email = {"from": "bcambel@gmail.com",
              "to": "bcambel@gmail.com",
              "subject": 'Subject',
              "text": 'text',
              "html": 'html or text'}


def test_new_mail():
  api_result = app_client.post("/mail",
                            data=base_email)

  print api_result
  result = json.loads(api_result.data)

  assert api_result.status == "200 OK"
  assert "id" in result and result['status'] == 'queued'

def test_new_mail_data():
  api_result = app_client.post("/mail",
                            data=base_email)

  print api_result
  result = json.loads(api_result.data)

  assert api_result.status == "200 OK"
  assert "id" in result and result['status'] == 'queued'

  mail_object_response = app_client.get("/mail/{}".format(result['id']))

  assert mail_object_response.status == "200 OK"
  result = json.loads(mail_object_response.data)
  assert "id" in result and result['status'] == 'queued'

def test_invalid_request_missing_to():
  missing_to = base_email.copy()
  del missing_to['to']
  api_result = app_client.post("/mail",
                            data=missing_to)

  print api_result.status
  assert api_result.status == "400 BAD REQUEST"

def test_invalid_request_invalid_email_to_address():
  missing_to = base_email.copy()
  missing_to['to'] = "bahadir@"
  api_result = app_client.post("/mail",
                            data=missing_to)

  print api_result.status
  api_json_result = json.loads(api_result.data)

  assert api_result.status == "400 BAD REQUEST"
  print api_json_result
  assert api_json_result['message'][0]['field'] == 'to'
  #{ 'message' : [{'field':'to' , 'message': "Email field 'to' is not a valid email address bahadir@"}]}

def test_missing_and_invalid_reported_together():
  missing_to = base_email.copy()
  del missing_to['from']
  missing_to['to'] = "bahadir@"
  api_result = app_client.post("/mail",
                            data=missing_to)

  print api_result.status
  api_json_result = json.loads(api_result.data)

  assert api_result.status == "400 BAD REQUEST"
  print api_json_result
  assert api_json_result['message'][0]['field'] == 'from'
  assert api_json_result['message'][1]['field'] == 'to'

def test_multiple_email_passes_validation():
  multiple_to = base_email.copy()
  multiple_to['to'] = ",".join(20*['bcambel@gmail.com'])

  api_result = app_client.post("/mail",
                            data=multiple_to)

  print api_result.data
  print api_result.status
  assert api_result.status == "200 OK"