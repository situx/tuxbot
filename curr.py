from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
from sopel.module import commands, example, NOLIMIT
from decimal import *
c = CurrencyRates()
b=BtcConverter()

@commands('curr\s([0-9]+(\.[0-9][0-9]?)?\s)?([A-z]+)\sin\s([A-z]+)','currency', 'exchange')
@example('.cur 20 EUR in USD')
def exchange(bot, trigger):
    fromcur=trigger.group(4).upper()
    tocur=trigger.group(5).upper()
    if trigger.group(2)==None:
        amount=Decimal(1.0) 
    else:
        amount=Decimal(trigger.group(2))
    if tocur=="BTC":
        bot.say(str(b.convert_to_btc(amount,fromcur)))
    else:
        bot.say("%.2f" % c.convert(fromcur,tocur,amount))

@commands('currate\s([A-z]+)')
def rate(bot,trigger):
    cur=trigger.group(2)
    bot.say(str(c.get_rates(cur)))
