from sortedcontainers import SortedDict
from forex_python.converter import CurrencyCodes
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
from sopel.module import commands, example, NOLIMIT
from decimal import *
from pymarketcap import Pymarketcap
from coinmarketcap import Market
import coinmarketcap
c = CurrencyRates()
b=BtcConverter()
m=Market()
cc=CurrencyCodes()
allcoins={}
curlist=list(c.get_rates("USD").keys())
#print(c.get_rates("USD"))
curlist.append("USD")
curlist.sort()
#print(curlist)
for cur in curlist:
    allcoins[cur]=cc.get_currency_name(cur)
altcoinmap={}
#print (coinmarketcap.price("BTC"))
json=m.ticker(convert='EUR')
#print(json)
for currency in json:
    altcoinmap[currency["symbol"]]=currency["id"]
    allcoins[currency["symbol"]]=currency["name"]
#print(altcoinmap)
#print(json)
#print(m.ticker("bitcoin",convert="EUR")[0]["price_usd"]*100)
allcoins=SortedDict(allcoins)
#print(allcoins)

@commands('curr\s([0-9]+(\.[0-9][0-9]?)?\s)?([A-z]+)\sin\s([A-z]+)')
@example('.curr 20 EUR in USD')
def exchange(bot, trigger):
    fromcur=trigger.group(4).upper()
    tocur=trigger.group(5).upper()
    if trigger.group(2)==None:
        amount=Decimal(1.0) 
    else:
        amount=Decimal(trigger.group(2))
    if fromcur==tocur:
        bot.say(str(amount)+" "+tocur)
    elif fromcur=="SATOSHI" and tocur in curlist:
        bot.say(str("%.2f "% (b.convert_btc_to_cur(amount,tocur)/100000000))+" "+tocur)
    elif fromcur=="BTC" and tocur in curlist:
        bot.say(str("%.2f "% b.convert_btc_to_cur(amount,tocur))+tocur)
    elif fromcur in curlist and tocur=="SATOSHI":
        bot.say(str("%.0f "% (b.convert_to_btc(amount,fromcur)*100000000))+tocur)
    elif fromcur in curlist and tocur=="BTC":
        bot.say(str("%.8f "% b.convert_to_btc(amount,fromcur))+tocur)
    elif fromcur in curlist and tocur in curlist:
        bot.say(str("%.2f" % c.convert(fromcur,tocur,amount))+tocur)
    elif fromcur not in curlist and fromcur in altcoinmap and tocur in curlist:
        usdamount=Decimal(m.ticker(altcoinmap[fromcur],convert="USD")[0]["price_usd"])*amount 
        print(usdamount)
        bot.say(str("%.2f "% c.convert("USD",tocur,usdamount))+" "+tocur)
    elif fromcur in curlist and tocur not in curlist and tocur in altcoinmap:
        usdamount=c.convert(fromcur,"USD",amount)
        factor=Decimal(m.ticker(altcoinmap[tocur],convert="USD")[0]["price_usd"])/usdamount
        bot.say(str("%.8f " % factor)+" "+tocur)
    else:
        bot.say("Due to an error, I currently cannot convert from "+fromcur+" to "+tocur)

@commands("curs")
def curs(bot,trigger):
    bot.reply("I am sending you the list of currencies in a private message!")
    counter=0
    line=""
    for curr in allcoins:
        if counter==5:
            bot.msg(trigger.nick,line)
            line=""
            counter=0
        else:
            line+=allcoins[curr]+"("+curr+") "
            counter+=1
    if counter!=0:
        bot.msg(trigger.nick,line)

@commands('currate\s([A-z]+)')
def rate(bot,trigger):
    cur=trigger.group(2)
    bot.say(str(c.get_rates(cur)))
