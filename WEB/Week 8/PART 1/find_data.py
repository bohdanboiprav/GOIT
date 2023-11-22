import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_quote_by_author(author: str):
    print("Author:")
    author = Author.objects(fullname=author).first()
    if author:
        quotes = Quote.objects(author=author)
        result = ', '.join([q.quote for q in quotes])
        return result
    else:
        return "Author not found"


@cache
def find_quote_by_tags(tags: str):
    tags = tags.split(",")
    result = []
    for i in tags:
        quotes = Quote.objects(tags=i)
        result.append(', '.join([q.quote for q in quotes]))
    return ', '.join(result)


mapper = {
    "name:": find_quote_by_author,
    "tag:": find_quote_by_tags,
    "tags:": find_quote_by_tags
}

if __name__ == '__main__':
    while True:
        command = input("Enter command: ")
        command = command.split(" ")
        if command[0] in mapper:
            print(mapper[command[0]](' '.join(command[1:])))
        if command[0] == "exit":
            break
