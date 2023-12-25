from fastapi import FastAPI, Path, Query
from mongoengine import *
import certifi
from pydantic import BaseModel

connect(
    db="web16",
    host="mongodb+srv://bohdanboiprav:5c7EeZfMyUi4hm1M@cluster0.qkace2s.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where())


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {"collection": "authors2"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=50))
    quote = StringField()
    meta = {"collection": "quotes2"}


app = FastAPI()


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/notes/new")
async def read_new_notes():
    return {"message": "Return new notes"}


# @app.get("/notes")
# async def read_notes(skip: int = 0, limit: int = 2):
#     authors = Author.objects.limit(limit).skip(skip)
#     return_data = []
#     for author in authors:
#         return_data.append({
#             "id": str(author.id),
#             "fullname": author.fullname,
#             "born_date": author.born_date,
#             "born_location": author.born_location,
#             "description": author.description
#         })
#     return return_data


# @app.get("/notes")
# async def read_notes(skip: int = 0, limit: int = Query(default=10, le=100, ge=10)):
#     return {"message": f"Return all notes: skip: {skip}, limit: {limit}"}


class Note(BaseModel):
    name: str
    description: str
    done: bool


@app.post("/notes")
async def create_note(note: Note):
    return {"name": note.name, "description": note.description, "status": note.done}
