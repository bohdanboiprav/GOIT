import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta
import json

DEFAULT_CURRENCY = ['EUR', 'USD']


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
                    currency: {'sale': next(x['saleRate'] for x in result['exchangeRate'] if x['currency'] == currency),
                               'purchase': next(
                                   x['purchaseRate'] for x in result['exchangeRate'] if x['currency'] == currency)}
                    for currency in DEFAULT_CURRENCY}}
                return proper_json_result


async def main(n_days, additional_currency=None):
    DEFAULT_CURRENCY.extend(additional_currency) if additional_currency else None
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
    r = asyncio.run(main(int(sys.argv[1]), sys.argv[2:]))
    print(r)
