"""
cleverbot.py - Cleverbot module for sopel bot
Copyright 2015, Timo Homburg
Licensed under GPL3.
"""
from sopel.module import rule, priority, rate
import HTMLParser
import cleverbot


cleverbot=cleverbot.Cleverbot()

@rule('tuxbot\:\s(.*)')
def goodbye(bot, trigger):
    h=HTMLParser.HTMLParser()    
    reply1=cleverbot.ask(trigger.group(1))
    if "|" in reply1:	
	reply1=reply1.replace("|","\\u").replace(".","").lower()
    bot.reply(h.unescape(unicode(reply1,"unicode_escape").encode("utf8")))  