from mongoengine import *
import certifi

connect(
    db="web16",
    host="",
    tlsCAFile=certifi.where())


class Task(Document):
    fullname = StringField(required=True)
    email_address = StringField(max_length=100)
    status = BooleanField(default=False)
    meta = {"collection": "tasks"}
