from ..config import db


class BotUser(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    tg_id = db.Column(db.BigInteger(), default=0)
    language = db.Column(db.Unicode(), max_length=2, default="ru")
