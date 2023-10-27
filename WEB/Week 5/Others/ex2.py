import asyncio


async def baz(num) -> str:
    print(f'{num} Before Sleep')
    await asyncio.sleep(2)
    #time.sleep(2)
    print(f'{num} After Sleep')
    return f'{num} Hello world'


async def main():
    r = []
    for i in range(1, 20):
        r.append(baz(i))
    await asyncio.gather(*r)


if __name__ == '__main__':
    asyncio.run(main())
