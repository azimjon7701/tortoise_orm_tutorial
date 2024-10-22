DATABASE = "tortoise_db"
HOST = "localhost"
PASSWORD = "password1"
PORT = "5432"
DBUSER = "tortoise_user"

ORM_CREDENTIALS = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": DATABASE,
                "host": HOST,
                "password": PASSWORD,
                "port": PORT,
                "user": DBUSER,
            },
        }
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "Asia/Tashkent"
}
