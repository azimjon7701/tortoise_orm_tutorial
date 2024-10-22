import asyncio

from tortoise import Tortoise

from models import User
from settings import ORM_CREDENTIALS


async def init_db():
    await Tortoise.init(config=ORM_CREDENTIALS)


async def create_user(username: str, email: str):
    user = await User.create(username=username, email=email)
    return user


async def get_user(user_id: int):
    user = await User.get(id=user_id)
    return user


async def update_user(user_id: int, username: str = None, email: str = None):
    user = await User.get(id=user_id)
    if username:
        user.username = username
    if email:
        user.email = email
    await user.save()
    return user


async def delete_user(user_id: int):
    user = await User.get(id=user_id)
    await user.delete()


async def main():
    await init_db() # har doim orm ishlashi uchun eng birinchi Tortoise.init qilish kerak
    new_user = await create_user(username="admin", email="admin@example.com")
    print(f"Yaratilgan foydalanuvchi: {new_user}")
    user = await get_user(new_user.id)
    print(f"Olingan foydalanuvchi: {user}")


if __name__ == "__main__":
    asyncio.run(main())
