"""
cleverbot.py - Costum commands for sopel bot
Credits to LangerJan for the idea
Copyright 2015, Timo Homburg
Licensed under GPL3.
"""
import sopel.module
import time
 
@sopel.module.commands('dance')
def helloworld(bot, trigger):
    bot.say('<(^.^<)')
    time.sleep(0.4)
    bot.say('<(^.^)>')
    time.sleep(0.4)
    bot.say('(>^.^)>')
    time.sleep(0.4)
    bot.say('(7^.^)7')
    time.sleep(0.4)
    bot.say('(>^.^<)')
