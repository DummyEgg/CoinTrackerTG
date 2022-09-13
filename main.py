import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import ChatType
from pycoingecko import CoinGeckoAPI
import ListGenerator


cg = CoinGeckoAPI()
cl = ListGenerator.generate()

API_TOKEN = ''

logging.basicConfig(level=logging.INFO)

cache = {} 

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


class Cache():
    def __init__(self, data = {}):
        self.data = data

    def getPrice(self, coin):
        if (coin in self.data):
            return self.data[coin]
        else:
            return None
    
    def getPrices(self, req):
        msg = []
        toSet = []
        for coin, cnt in req:
            t = self.getPrice(self, coin)
            if (t != None):
                msg.append([coin, cnt, t])
            else:
                toSet.append([coin, cnt])
        self.setPrices(self, toSet)

    async def setPrices(self, toSet):
        ids = []
        for id, _ in toSet:
            ids.append(id)

        t = await cg.get_price(ids=ids, vs_currencies='usd', include_24hr_change=True)
        for coin in t:
            self.data[coin] = t[coin]
            await(60)
            self.data.pop(coin, None)

    

def parseAndRequest():
    pass

@dp.message_handler(chat_type=[ChatType.PRIVATE, ChatType.SUPERGROUP, ChatType.all])
async def send_welcome(message: types.Message):
    #await message.reply("Hi\n your message was " + message.text)
    response = parseAndRequest(message.text)
    if response != []:
        await message.reply(response)
    raise SkipHandler



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
