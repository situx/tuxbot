import xml.etree.ElementTree as ET
from decimal import *
import collections
from sopel.module import commands, example, NOLIMIT
from curr import curconvert

wordhash={}
credithash={}
initialvalue=100000.00

def setup(bot):
    e = ET.parse('/home/bananapi/.sopel/modules/invest.xml').getroot()
    for atype in e.findall('user'):
        wordhash[atype.get('name')]={}
        for child in atype.iter('cur'):
            wordhash[atype.get('name')][child    .get('currency')]=child.get('value')
    print(str(wordhash))

@commands('investstart')
def startinvest(bot,trigger):
    user=trigger.nick
    wordhash[user]={}
    wordhash[user]["EUR"]=initialvalue
    bot.reply("I created an investment portfolio for you. Your initial investment funds are "+str(initialvalue)+"EUR")
    toxml()

@commands('curvalue(\s(.*))?')
def currentvalue(bot,trigger):
    user=trigger.nick
    print(trigger.group(3))
    if trigger.group(3):
        user=trigger.group(3)
        print(user)
    if user not in wordhash:
        bot.say("You need to create a new portfolio first. Use the .investstart command to get started!")
        return
    result=Decimal(0)
    for curkey,val in wordhash[user].items():
        result+=Decimal(curconvert(curkey,"EUR",Decimal(val)))
    bot.reply("Current value of "+user+"'s whole portfolio in EUR is "+str("%.2f "%result)+"EUR")
    print(str(wordhash))

@commands('investstatus')
def investstatus(bot,trigger):
    user=trigger.nick
    for curkey,val in sorted(wordhash[user].items()):
        if curkey=="EUR":
            bot.say(str("%.2f "%float(val))+curkey)
        else:
            bot.say(str("%.8f "%float(val))+curkey)

@commands('sell\s([0-9]+\.?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?)\s([A-z]+)')
def sell(bot,trigger):
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
def buy(bot,trigger):
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
    tree.write('invest.xml')    
