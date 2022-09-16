import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import ChatType
from pycoingecko import CoinGeckoAPI
import ListGenerator
from time import sleep
cg = CoinGeckoAPI()

cl = ListGenerator.generate()

API_TOKEN = '853797580:AAERBp57OwmpnMGFzQ7NfuiNl7sH-7RT7f8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


class Cache():
    def __init__(self, data = {}):
        self.data = data

    async def getPrice(self, coin):
        if (coin in self.data):
            return self.data[coin]
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
            print(self.data['bitcoin'])
            if t:
                msg.append([coin, cnt, t])
        return msg
            

    async def setPrices(self, toSet):
        ids = []
        for id, _ in toSet:
            ids.append(id)
        t = cg.get_price(ids=ids, vs_currencies='usd', include_24hr_change=True)
        for coin in t:
            if (t[coin] != {}):
                self.data[coin] = t[coin]
                print(self.data['bitcoin'])
                await sleep(60)
                self.data.pop(coin, None)
                 

    
cache = Cache()


async def parseAndRequest(message):
    m = message.split()
    q = []
    for i in range(0, len(m)-1):
        nw = m[i]
        if (nw.isnumeric()):
            cnt = int(nw)
            coin = m[i+1]
            if (coin == 'btc'):
                print(cl[coin])
            if (coin in cl and cl[coin] != coin):
                q.append([cl[coin], cnt])
            q.append([coin, cnt])
    
    return await cache.getPrices(q)



@dp.message_handler(chat_type=[ChatType.PRIVATE, ChatType.SUPERGROUP, ChatType.all])
async def send_welcome(message: types.Message):
    #await message.reply("Hi\n your message was " + message.text)
    response = await parseAndRequest(message.text)
    if response != []:
        await message.reply(response)
    raise SkipHandler



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
