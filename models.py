from datetime import datetime
import uuid
import json
from app import db


class Statuses:
  queued = "queued"
  inprogress = "inprogress"
  success = "success"
  error = "error"

class Email(db.Model):
  id = db.Column(db.String(36),primary_key=True, default=uuid.uuid4)
  status = db.Column(db.String(10))

  from_address = db.Column(db.String(100))
  to_address = db.Column(db.String(1000))
  subject = db.Column(db.String(1000))
  mail = db.Column(db.String(1000))
  result = db.Column(db.Text)

  created_at = db.Column(db.Date, default=datetime.utcnow)
  updated_at = db.Column(db.Date, default=datetime.utcnow)

  def as_dict(self):
    d = {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    try:
      d['result'] = json.loads(d['result'])
    except:
      pass
    return d

  @classmethod
  def insert(cls, data):
    eq = Email()
    eq.id = str(uuid.uuid4())
    eq.status = Statuses.queued
    eq.from_address = data.get("from")
    eq.to_address = data.get("to")
    eq.subject = data.get("subject")
    eq.mail = data.get('text')

    db.session.add(eq)

    db.session.commit()

    return eq.id

  @classmethod
  def by_id(cls, id):
    return Email.query.get(id)
