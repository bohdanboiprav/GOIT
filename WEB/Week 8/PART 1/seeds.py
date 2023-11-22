import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote

if __name__ == '__main__':
    with (open("authors.json", "r") as fh):
        data = json.load(fh)
        for el in data:
            try:
                author = Author(fullname=el["fullname"], born_date=el["born_date"], born_location=el["born_location"],
                                description=el["description"])
                author.save()
            except NotUniqueError:
                pass
    with open("qoutes.json", "r") as fh:
        data = json.load(fh)
        for el in data:
            try:
                author = Author.objects(fullname=el["author"]).first()
                quote = Quote(author=author, tags=el["tags"], quote=el["quote"])
                quote.save()
            except NotUniqueError:
                pass
