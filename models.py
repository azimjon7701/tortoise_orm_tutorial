from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100)
    bio = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "users"  # table_name