import os

import django
from quotesapp.models import Author, Quote, Tag
from mongoengine import *
import certifi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

connect(
    db="web16",
    host="mongodb+srv://bohdanboiprav:*****@cluster0.qkace2s.mongodb.net/",
    tlsCAFile=certifi.where())


class AuthorM(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {"collection": "authors3"}


class QuoteM(Document):
    author = ReferenceField(AuthorM, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=50))
    quote = StringField()
    meta = {"collection": "quotes3"}


for new_author in AuthorM.objects.all():
    author_obj = Author.objects.create(fullname=new_author.fullname, born_date=new_author.born_date,
                                       born_location=new_author.born_location,
                                       description=new_author.description)
    for new_quote in QuoteM.objects.all():
        quote_obj = Quote.objects.create(author=author_obj, quote=new_quote.quote)
        for new_tag in new_quote.tags:
            tag_obj, created = Tag.objects.get_or_create(name=new_tag)
            quote_obj.tags.add(tag_obj)