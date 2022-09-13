from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def generate():
    list = cg.get_coins_list()
    d = {}
    for obj in list:
        d[obj['symbol']] = obj['id']
    return d