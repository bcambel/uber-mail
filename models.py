from datetime import datetime
import uuid
from app import db

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
    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

  @classmethod
  def insert(cls, **kwargs):
    eq = Email()
    eq.id = str(uuid.uuid4())
    eq.status = "queued"
    eq.from_address = kwargs.get("from")
    eq.to_address = kwargs.get("to")
    eq.subject = kwargs.get("subject")
    eq.mail = kwargs.get('text')

    db.session.add(eq)

    db.session.commit()

    return eq.id

  @classmethod
  def by_id(cls, id):
    return Email.query.get(id)
