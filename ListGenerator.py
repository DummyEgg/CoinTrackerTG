from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


async def generate():
    list = cg.get_coins_list()
    d = {}
    for obj in list:
        if obj['symbol'] in d:
            d[obj['symbol']].append(obj['id'])
        else:
            d[obj['symbol']] = [obj['id']]
    return d