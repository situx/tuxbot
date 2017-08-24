import sopel

@sopel.module.commands('ps?\s+(.+)')

def phantomspeak(bot,trigger):
    zsign=trigger.group(2)
    bot.say(zsign)



