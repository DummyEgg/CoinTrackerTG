import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import ChatType
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

API_TOKEN = '5176920749:AAH1vevXt8M8v4OpcVIbwWmZApZKnO3m9us'

logging.basicConfig(level=logging.INFO)

cache = {"coin" : []} 

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

def checkCoin():
    pass

def addCoin():
    pass


def parseAndRequest(s):
    words = s.split(" ")
    reqv = []
    for i in range(0, len(words)- 1):
        if words[i].isnumeric():
            cnt = int(words[i])
            coin = words[i+1]
            reqv.append([coin, cnt])

    msg = []
    for coin, cnt in reqv:
        if checkCoin(coin):
            tmp = cg.get_price(ids=coin, vs_currencies='usd')
            if tmp != {}:
                msg.append([coin, tmp[coin]['usd'] * cnt])
                addCoin(coin, tmp[coin]['usd'])
    return msg

    

@dp.message_handler(chat_type=[ChatType.PRIVATE, ChatType.SUPERGROUP, ChatType.all])
async def send_welcome(message: types.Message):
    #await message.reply("Hi\n your message was " + message.text)
    response = parseAndRequest(message.text)
    await message.reply(response)
    raise SkipHandler



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
