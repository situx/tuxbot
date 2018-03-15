import xml.etree.ElementTree as ET
from decimal import *
import collections
from sopel.module import commands, example, NOLIMIT
from sortedcontainers import SortedDict
from forex_python.converter import CurrencyCodes
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
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

wordhash={}
credithash={}
initialvalue=100000.00

investfile = '/home/bananapi/.sopel/modules/invest.xml'

def setup(bot):
    e = ET.parse(investfile).getroot()
    for atype in e.findall('user'):
        wordhash[atype.get('name')]={}
        for child in atype.iter('cur'):
            wordhash[atype.get('name')][child.get('currency')]=child.get('value')
    print(str(wordhash))

@commands('investstart','startinvest')
@example('.investstart','.startinvest')
def startinvest(bot,trigger):
    """Starts and/or resets an initial investment portfolio"""
    user=trigger.nick
    wordhash[user]={}
    wordhash[user]["EUR"]=initialvalue
    bot.reply("I created an investment portfolio for you. Your initial investment funds are "+str(initialvalue)+"EUR")
    toxml()

@commands('curvalue(\s(.*))?')
@example('.curvalue','.curvalue nick')
def currentvalue(bot,trigger):
    """Prints the current value of the portfolio of the given user in EUR"""
    user=trigger.nick
    if trigger.group(3):
        user=trigger.group(3)
    if user not in wordhash:
        bot.say("You need to create a new portfolio for "+user+" first. Use the .investstart command to get started!")
        return
    result=Decimal(0)
    for curkey,val in wordhash[user].items():
        result+=Decimal(curconvert(curkey,"EUR",Decimal(val)))
    bot.reply("Current value of "+user+"'s whole portfolio in EUR is "+str("%.2f "%result)+"EUR")
    print(str(wordhash))

@commands('investstatus(\s(.*))?')
@example('.investstatus','.investstatus nick')
def investstatus(bot,trigger):
    user=trigger.nick
    if (trigger.group(3)):
        user=trigger.group(3)
    if user not in wordhash:
        return
    for curkey,val in sorted(wordhash[user].items()):
        if curkey=="EUR":
            bot.say(str("%.2f "%float(val))+curkey)
        else:
            bot.say(str("%.8f "%float(val))+curkey)

@commands('sell\s([0-9]+\.?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?)\s([A-z]+)')
@example('.sell 10.56 BTC')
def sell(bot,trigger):
    """Sells the specified amount in the specified currency from the virtual portfolio"""
    amount=Decimal(trigger.group(2))
    currency=trigger.group(3).upper()
    user=trigger.nick
    if not user in wordhash:
        bot.say("You need to create a new portfolio first. Use the .investstart command to get started!")
        return
    btcineur=Decimal(curconvert(currency,"EUR",amount))
    if amount>Decimal(wordhash[user][currency]):
        bot.reply("You do not have enough "+currency+" to sell this amount. You only have "+str(wordhash[user][currency]))
    else:
        wordhash[user]["EUR"]=Decimal(wordhash[user]["EUR"])+btcineur
        wordhash[user][currency]=Decimal(wordhash[user][currency])-amount
        bot.reply("You sold "+str(amount)+currency+" and got "+str("%.2f "%(btcineur))+" EUR!")
        bot.reply("Your EUR balance is now: "+str("%.2f "%wordhash[user]["EUR"])+"EUR")
    toxml()

@commands('buy\s([0-9]+\.?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?)\s([A-z]+)')
@example('.buy 5 BTC')
def buy(bot,trigger):
    """Buys the specified amount of money in the specified currency given enough budget is available in the portfolio"""
    amount=Decimal(trigger.group(2))
    currency=trigger.group(3).upper()
    user=trigger.nick
    if user not in wordhash:
        bot.say("You need to create a new portfolio first. Use the .investstart command to get started!")
        return
    euramount=Decimal(wordhash[user]["EUR"])
    btcineur=curconvert(currency,"EUR",amount)
    if btcineur>euramount:
        bot.reply("You do not have enough EUR to buy "+str(amount)+" "+currency)
    else:
        wordhash[user]["EUR"]=Decimal(wordhash[user]["EUR"])-btcineur
        if not currency in wordhash[user]:
            wordhash[user][currency]=Decimal(0)
        wordhash[user][currency]=Decimal(wordhash[user][currency])+Decimal(amount)
        bot.reply("You purchased "+str(amount)+currency+". Your "+currency+" balance is now "+str(wordhash[user][currency])+currency)
        bot.reply("Your EUR balance is now: "+str("%.2f "%wordhash[user]["EUR"])+"EUR")
    toxml();

def toxml():
    root = ET.Element('data')
    for key in wordhash:
        user=ET.SubElement(root,'user')
        user.set("name",key)
        for curkey,val in wordhash[key].items():
            curtag=ET.SubElement(user,'cur')
            curtag.set('currency',curkey)
            curtag.set('value',str(val))
    tree=ET.ElementTree(root)
    tree.write(investfile)    

def curconvert(fromcur,tocur,amount):
    if amount==None:
        amount=Decimal(1.0) 
    if fromcur==tocur:
        return amount
    elif fromcur=="SATOSHI" and tocur in curlist:
        return b.convert_btc_to_cur(amount,tocur)/100000000
    elif fromcur=="BTC" and tocur in curlist:
        return b.convert_btc_to_cur(amount,tocur)
    elif fromcur in curlist and tocur=="SATOSHI":
        return b.convert_to_btc(amount,fromcur)*100000000
    elif fromcur in curlist and tocur=="BTC":
        return b.convert_to_btc(amount,fromcur)
    elif fromcur in curlist and tocur in curlist:
        return c.convert(fromcur,tocur,amount)
    elif fromcur not in curlist and fromcur in altcoinmap and tocur in curlist:
        usdamount=Decimal(m.ticker(altcoinmap[fromcur],convert="USD")[0]["price_usd"])*amount 
        #print(usdamount)
        return c.convert("USD",tocur,usdamount)
    elif fromcur in curlist and tocur not in curlist and tocur in altcoinmap:
        #print(str(amount)+" "+fromcur)
        usdamount=c.convert(fromcur,"USD",amount)
        #print("USDAmount: "+str(usdamount))
        factor=usdamount/Decimal(m.ticker(altcoinmap[tocur],convert="USD")[0]["price_usd"])
        return factor#print("Factor: 1"+tocur+"="+str(m.ticker(altcoinmap[tocur],convert="USD")[0]["price_usd"])))
    else:
        return None

@commands('curr\s([0-9]+(\.[0-9][0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?)?\s)?([A-z]+)\sin\s([A-z]+)')
@example('.curr 20 EUR in USD')
def exchange(bot, trigger):
    """Prints the current exchange rate for the two given currencies"""
    fromcur=trigger.group(4).upper()
    tocur=trigger.group(5).upper()
    if trigger.group(2)==None:
        amount=Decimal(1.0) 
    else:
        amount=Decimal(trigger.group(2))
    if fromcur==tocur:
        bot.say(str(amount)+" "+tocur)
    elif fromcur=="SATOSHI" and tocur in curlist:
        bot.say(str("%.2f "% (curconvert(fromcur,tocur,amount)+tocur)))
    elif fromcur=="BTC" and tocur in curlist:
        bot.say(str("%.2f "% (curconvert(fromcur,tocur,amount))+tocur))
    elif fromcur in curlist and tocur=="SATOSHI":
        bot.say(str("%.0f "% (curconvert(fromcur,tocur,amount))+tocur))
    elif fromcur in curlist and tocur=="BTC":
        bot.say(str("%.8f "% (curconvert(fromcur,tocur,amount))+tocur))
    elif fromcur in curlist and tocur in curlist:
        bot.say(str("%.2f " % (curconvert(fromcur,tocur,amount))+tocur))
    elif fromcur not in curlist and fromcur in altcoinmap and tocur in curlist:
        bot.say(str("%.2f "% (curconvert(fromcur,tocur,amount))+tocur))
    elif fromcur in curlist and tocur not in curlist and tocur in altcoinmap:
        bot.say(str("%.8f " % (curconvert(fromcur,tocur,amount))+tocur))
    else:
        bot.say("Due to an error, I currently cannot convert from "+fromcur+" to "+tocur)

@commands("curs")
@example(".curs")
def curs(bot,trigger):
    """Prints a list of available currencies in a private message"""
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

@commands('currate\s+([A-z]+)')
@example('.currate currency')
def rate(bot,trigger):
    cur=trigger.group(2)
    bot.say(str(c.get_rates(cur)))
