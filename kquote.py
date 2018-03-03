import xml.etree.ElementTree as ET
import sopel.module
import random

quotehash={}

def setup(bot):
    e = ET.parse('/home/bananapi/.sopel/modules/kquote.xml').getroot()
    for atype in e.findall('quote'):
        quotehash[atype.get('author')]=atype.text


@sopel.module.commands('kquote')
@sopel.module.example('.kquote')
def wortspielcredit(bot,trigger):
    """Prints a random quote from the kquote repository"""
    choose=random.choice(list(quotehash.keys()))
    bot.say(quotehash[choose])
    bot.say(choose)
