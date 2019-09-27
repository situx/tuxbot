import sopel.module
import time

@sopel.module.commands('dance')
@sopel.module.example('.dance')
def helloworld(bot, trigger):
    """Lets the bot execute a dancing script"""
    bot.say('<(^.^<)')
    time.sleep(0.4)
    bot.say('<(^.^)>')
    time.sleep(0.4)
    bot.say('(>^.^)>')
    time.sleep(0.4)
    bot.say('(7^.^)7') 
    time.sleep(0.4)
    bot.say('(>^.^<)')

@sopel.module.rule('^\s*[Mm]+[Oo]+[Ii]+[Nn]+\s*$')
@sopel.module.example('Moin','moin')
def moin(bot,trigger):
    """Lets the bot reply to a greeting"""
    bot.say('moin')
    
@sopel.module.rule('^\s*[Dd]roggelbecher([?!]+)\s*$')
@sopel.module.example('Droggelbecher')
def droggelbecher(bot,trigger):
    """Replys Droggelbecher"""
    if "?" in trigger.group(2):
        bot.say('Droggelbecher!')
    elif "!" in trigger.group(2):
        bot.say('Droggelbecher?')
    else:
        bot.say('Droggelbecher')
