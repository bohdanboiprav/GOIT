import concurrent.futures
import logging
from random import randint
from time import sleep, time


def greeting(name):
    logging.debug(f'greeting for: {name}')
    sleep(2)
    return f"Hello {name}"


arguments = (
    "Bill",
    "Jill",
    "Till",
    "Sam",
    "Tom",
    "John",
)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    start_time = time()
    results = map(greeting, arguments)
    print(list(results))
    logging.debug(f"Time taken: {time() - start_time}")

    logging.debug(results)
