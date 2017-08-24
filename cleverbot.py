#coding: utf8
"""
ai.py - Artificial Intelligence Module
Copyright 2009-2011, Michael Yanovich, yanovich.net
Licensed under the Eiffel Forum License 2.
http://sopel.chat
"""
from cleverwrap import CleverWrap
from sopel.module import rule, priority, rate
import random
import time
#import aiml
import os
import html.parser
import cleverbot

#kernel=aiml.Kernel()
#cleverbot=cleverbot.Cleverbot('cleverbot-py-example')
cleverbot=CleverWrap("830d8fe7b7ad941487e46f593af70370","tuxbot")
#def setup(bot):
   # if os.path.isfile("bot_brain.brn"):
    #    kernel.bootstrap(brainFile = "bot_brain.brn")
    #else:
    #    kernel.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
    #    kernel.saveBrain("bot_brain.brn")
    # Set value to 3 if not configured
#    if bot.config.ai and bot.config.ai.frequency:
#        bot.memory['frequency'] = bot.config.ai.frequency
#    else:
#        bot.memory['frequency'] = 3
#
#    random.seed()


#def decide(bot):
#    return 0 < random.random() < float(bot.memory['frequency']) / 10

@rule('tuxbot[\:：]\s(.*)')
#@rate(30)
def goodbye(bot, trigger):
    #if "?" in trigger.group(1):
#    bot.say("thinking.....")
    reply1=cleverbot.say(trigger.group(1))
    #print(reply1)
    if "|" in reply1:
     reply1=html.unescape(reply1).encode('utf8').replace("|","\\u").replace(".","").lower()
    bot.reply(reply1)
    #bot.reply(html.unescape(bytes(reply1,"utf-8").decode("unicode_escape")))
    #else:
    #   bot.reply(kernel.respond(trigger.group(1)))
