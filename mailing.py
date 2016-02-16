import json
import logging
import requests
import sendgrid
import time

# in order to stop InsecureRequestWarnings
# http://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
requests.packages.urllib3.disable_warnings()

class Postman(object):

  def __init__(self, **settings):
    self.active = self.mailgun = MailGunPostman(settings['mailgun_key'], settings['mailgun_domain'])
    self.alternate = self.sendgrid = SendGridPostman(settings['sendgrid_key'])


  def deliver(self, from_email, to, subject, text, html=None):
    "Uses the active email gateway to send an email"
    logging.info("Deliver {} with {}".format(to,subject))
    primary_response = self.active.deliver(from_email, to, subject, text)

    return primary_response

  def switch(self):
    """
    Switches active email provider with the alternate one.
    """
    self.active, self.alternate = self.alternate, self.active


class MailGunPostman(Postman):
  """
  Mailgun Mail service integration.
  """
  def __init__(self, api_key, domain):
    self.domain = domain
    self.api_key = api_key

  def deliver(self, from_email, to, subject, text, html=None):
    send_result = requests.post("https://api.mailgun.net/v3/{}/messages".format(self.domain),
          auth=("api", self.api_key),
          data={"from": from_email,
                "to": to,
                "subject": subject,
                "text": text,
                "html": html or text}, verify=False)

    logging.debug("Sent resulted in {} :\n{}".format(send_result.status_code, send_result.text))

    try:
      message = send_result.json()
    except ValueError:
      message = send_result.text

    return {'status': send_result.status_code,
            'success': send_result.ok,
            'result' : message,
            'via': type(self).__name__,
            'ts' : int(time.time())}



class SendGridPostman(Postman):
  """
  SendGrid mail service integration.
  """
  def __init__(self, api_key):
    self.api_key = api_key
    self.sg = sendgrid.SendGridClient(self.api_key)

  def deliver(self, from_email, to, subject, text, html=""):
    message = sendgrid.Mail()
    message.add_to(to)
    message.set_subject(subject)
    message.set_html(html)
    message.set_text(text)
    message.set_from(from_email)
    status, msg = self.sg.send(message)

    # sendgrid reports 429 if Rate Limit exceeded.

    return {'status' : status,
            'success' : 200 <= status < 300,
            'result': json.loads(msg),
            'via': type(self).__name__,
            'ts' : int(time.time())}
