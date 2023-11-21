import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote

def find_quote_by_author(author: str):
    author = Author.objects(fullname=author).first()
    if author:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(quote.quote)
    else:
        print("Author not found")