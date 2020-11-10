import asyncio
from ..config import db


class BotUser(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    tg_id = db.Column(db.BigInteger())
    token = db.Column(db.Unicode(), default="", max_length=256)
    lang = db.Column(db.Unicode(), max_length=2, default="ru")

async def main():
    await db.set_bind('postgresql://localhost/gino')
    await db.gino.create_all()

    # further code goes here

    await db.pop_bind().close()

asyncio.get_event_loop().run_until_complete(main())