from aiopath import AsyncPath
from aiofile import async_open
from datetime import datetime


async def main():
    apath = AsyncPath("exchange_request_history.txt")
    async with async_open(apath, 'a+') as afp:
        await afp.write(f"Exchange rate request at {datetime.now()}\n")
