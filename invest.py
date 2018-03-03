import xml.etree.ElementTree as ET
from decimal import *
import collections
from sopel.module import commands, example, NOLIMIT
from curr import *

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

@commands('investstart')
@example('.investstart')
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
