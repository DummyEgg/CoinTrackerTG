import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import ChatType
from pycoingecko import CoinGeckoAPI
import ListGenerator
import asyncio, datetime
from dotenv import load_dotenv, dotenv_values
import re

load_dotenv()
config = dotenv_values('.env')

cg = CoinGeckoAPI()

cl = {}

UPDATE_TIME = 3600*24

async def updateCoinList():
    while True:
        global cl
        cl = await ListGenerator.generate()
        await asyncio.sleep(UPDATE_TIME)


API_TOKEN = config['API_TOKEN']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

class Cache():
    def __init__(self, data = {}):
        self.data = data

    async def getPrice(self, coin):
        if (coin in self.data):
            lastChecked = self.data[coin][1]
            now = datetime.datetime.now()
            delta = now-lastChecked
            deltaS = delta.total_seconds()
            logging.debug(f"difference {deltaS}")
            if (deltaS >= 60):
                return None
            return self.data[coin][0]
        else:
            return None
    
    async def getPrices(self, req):
        msg = []
        toSet = []
        for coin, cnt in req:
            t = await self.getPrice(coin)
            if (t != None):
                msg.append([coin, cnt, t])
            else:
                toSet.append([coin, cnt])
        await self.setPrices(toSet)
        for coin, cnt in toSet:
            t = await self.getPrice(coin)
            if t:
                msg.append([coin, cnt, t])
        return msg
            

    async def setPrices(self, toSet):
        ids = [id for id, _ in toSet]
        t = cg.get_price(ids=ids, vs_currencies='usd', include_24hr_change=True)
        for coin in t:
            if (t[coin] != {}):
                now = datetime.datetime.now()
                self.data[coin] = [t[coin], now]
                 

    
cache = Cache()

async def parseAndRequest(message):
    r = re.findall('[0-9.]+\s[a-zA-Z0-9]{1,}', message)
    if r is None:
        return []
    q = []
    for st in r:
        s = st.split()[::-1]
        coin = s[0].lower()
        cnt = s[1]
        q.append([coin, cnt])
        if coin in cl and cl[coin] != coin:
            q.append([cl[coin], cnt])
    return await cache.getPrices(q)


def beautifulResponse(coins):
    msg = f""""""
    for coin,cnt,t in coins:
        change = t['usd_24h_change']
        change = "{:.2f}".format(change)
        if (change[0] != '-'):
            change = "+" + change
        msg += f"``` {cnt} {coin}:```"
        msg += f"``` {t['usd']*float(cnt)} usd\t\t | {change}% ```"
        msg += "\n"
    return msg

#([{coin}](https://coingecko.com/en/coins/{coin}))

@dp.message_handler(chat_type=[ChatType.PRIVATE, ChatType.SUPERGROUP, ChatType.all])
async def send_welcome(message: types.Message):
    #await message.reply("Hi\n your message was " + message.text)
    response = await parseAndRequest(message.text)
    if response != []:
        await message.reply(beautifulResponse(response), parse_mode='MARKDOWN')
    raise SkipHandler



async def main():
    
    tasks = [
        asyncio.create_task(updateCoinList()),
        dp.start_polling()
    ]
    
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
    
