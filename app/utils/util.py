from db.tables import users
from db.database import database


async def check_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if not user:
        return False
    return True
