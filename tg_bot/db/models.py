import asyncio
from tortoise.models import Model
from tortoise import fields


class BotUser(Model):
    tg_id = fields.BigIntField(default=0)
    token = fields.CharField(max_length=256, default="")
    lang = fields.CharField(max_length=2, default="ru")

    def __str__(self):
        return self.tg_id


class Group(Model):
    tg_id = fields.BigIntField(default=0)
    admin = fields.ForeignKeyField("models.BotUser", "groups")

    def __str__(self):
        return self.tg_id

# class Subscriber(Model):
#     id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
#     tg_id = db.Column(db.BigInteger())
#     token = db.Column(db.Unicode(), default="", max_length=256)
#     lang = db.Column(db.Unicode(), max_length=2, default="ru")

# aerich init -t config.TORTOISE_ORM && aerich init-db && aerich migrate && aerich upgrade && 