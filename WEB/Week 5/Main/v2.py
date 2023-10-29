import aiohttp
import asyncio
from datetime import datetime, timedelta
import json
import sys


class DateException(Exception):
    pass


class HttpError(Exception):
    pass


async def request(url, session):
    async with session.get(url) as response:
        result = await response.json()
        proper_json_result = {result['date']: {
            'EUR': {
                'sale': result['exchangeRate'][8]['saleRate'],
                'purchase': result['exchangeRate'][8]['purchaseRate']
            },
            'USD': {
                'sale': result['exchangeRate'][23]['saleRate'],
                'purchase': result['exchangeRate'][23]['purchaseRate']
            }}}
        return proper_json_result


async def main(n_days):
    if n_days > 10:
        raise DateException("Too many days")
    return_dates = [datetime.strftime(datetime.now() - timedelta(days=i), '%d.%m.%Y') for i in range(n_days)]
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        result = await asyncio.gather(*map(lambda x:
                                           request(f'https://api.privatbank.ua/p24api/exchange_rates?date={x}',
                                                   session),
                                           return_dates[::-1]))

        pretty_json_result = json.dumps(result, indent=4)
        return pretty_json_result


if __name__ == "__main__":
    r = asyncio.run(main(int(sys.argv[1])))
    print(r)
