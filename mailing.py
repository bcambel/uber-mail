import logging
import requests
import sendgrid

class Postman(object):

  def __init__(self, **settings):
    self.default = MailGunPostman(settings['mailgun_key'], settings['mailgun_domain'])
    self.alternate = SendGridPostman(settings['sendgrid_key'])
    self.active = self.default

  def deliver(self, from_email, to, subject, text):
    logging.info("Deliver {} with {}".format(to,subject))
    primary_response = self.active.deliver(from_email, to, subject, text)


class MailGunPostman(Postman):
  """
  Mailgun Mail service integration.
  """
  def __init__(self, api_key, domain):
    self.domain = domain
    self.api_key = api_key

  def deliver(self, from_email, to, subject, text):
    send_result = requests.post("https://api.mailgun.net/v3/{}/messages".format(self.domain),
          auth=("api", self.api_key),
          data={"from": from_email,
                "to": to,
                "subject": subject,
                "text": text}, verify=False)

    return send_result.ok


class SendGridPostman(Postman):
  """
  SendGrid mail service integration.
  """
  def __init__(self, api_key):
    self.sg = sendgrid.SendGridClient(api_key)

  def deliver(self, from_email, to, subject, text, html=""):
    message = sendgrid.Mail()
    message.add_to(to)
    message.set_subject(subject)
    message.set_html(html)
    message.set_text(text)
    message.set_from(from_email)
    status, msg = self.sg.send(message)
    return status, msg