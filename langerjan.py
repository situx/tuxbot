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

@sopel.module.rule('^[Mm]oin$')
def moin(bot,trigger):
    bot.say('moin')
