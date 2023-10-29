import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta
import json


class DateException(Exception):
    pass


class HttpError(Exception):
    pass


async def request(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            if response.status == 200:
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
    try:
        return_list = []
        return_dates = [datetime.strftime(datetime.now() - timedelta(days=i), '%d.%m.%Y') for i in range(n_days)]
        for i in return_dates[::-1]:
            response = request(f'https://api.privatbank.ua/p24api/exchange_rates?date={i}')
            return_list.append(response)
        result = await asyncio.gather(*return_list)
        pretty_json_result = json.dumps(result, indent=4)
        return pretty_json_result
    except HttpError as er:
        print(er)


if __name__ == "__main__":
    r = asyncio.run(main(int(sys.argv[1])))
    print(r)
