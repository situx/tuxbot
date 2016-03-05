"""
cleverbot.py - Costum commands for sopel bot
Copyright 2015, Timo Homburg
Licensed under GPL3.
"""
from sopel import module
from random import randint

@module.rule('(:[-]?\/|m\(|:[-]?\\\\|:[-]?\()')
def hi(bot, trigger):
    if trigger.nick=="eintopf" and (trigger.group(1)==":(" or trigger.group(1)==":-("):
	switcher = {
        	0: "emotopf",
        	1: "Don't worry, be happy!",
        	2: "/me slaps "+trigger.nick,
    		3: "Das Pferd frisst keinen Gurkensalat",
		4: "/me hugs "+trigger.nick,
		5: "have a kitten: http://www.emergencykitten.com/",
		6: "poor "+trigger.nick+": https://www.youtube.com/watch?v=oHg5SJYRHA0",
		7: "Lets have a drink some time",
		8: "<3",
		9: ":-*",
		10: ":-((",
		11: "/me tickles "+trigger.nick
	}
	rand=randint(0,len(switcher)+6)
	if rand>=len(switcher):
		bot.say(trigger.group(1))
	else:
		bot.say(switcher[rand])
    else: 
    	#if trigger.nick=="eintopf" or trigger.nick=="LangerJan" or trigger.nick=="kaner" or trigger.nick=="situx":
	bot.say(trigger.group(1))

@module.commands('snack')
def snack(bot, trigger):
    bot.say('Nomnomnom')

@module.commands('ping')
def helloworld(bot, trigger):
    bot.say('pong')

