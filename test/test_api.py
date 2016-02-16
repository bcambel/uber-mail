import json
import logging
import requests

from app import *

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