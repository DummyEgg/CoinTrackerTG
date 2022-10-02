import json

class Currency:
    def __init__(self):
        self.data = {}

    def addChat(self, chatId):
        self.data[chatId] = {'usd'} #default currency : usd

    def addCurrency(self, chatId, currencyList):
        for c in currencyList:
            if c not in self.data[chatId]:
                self.data[chatId].add(c)
            #with open("currency_data.json", "w") as file:
    
    def deleteCurrency(self, chatId, currencyList):
        for c in currencyList:
            self.data[chatId].discard(c)

    def getCurrency(self, chatId):
        if chatId in self.data:
            return self.data[chatId]