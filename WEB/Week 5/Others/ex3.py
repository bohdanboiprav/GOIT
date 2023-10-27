import asyncio
import random
from timming import async_timed, sync_timed


async def random_value():
    print("start task")
    await asyncio.sleep(5)
    print("task finished")
    return random.random()


async def random_sum():
    print("start task")
    await asyncio.sleep(5)
    print("task finished")
    return random.random() + random.random()


@async_timed()
async def main():
    task = asyncio.create_task(random_value())
    task2 = asyncio.create_task(random_sum())
    print("task scheduled")
    await task2, task
    print(f"result: {task.result()}")
    print(f"result: {task2.result()}")


if __name__ == '__main__':
    asyncio.run(main())
