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

@module.commands('github')
@module.example('.github')
def github(bot,trigger):
    """Prints the bots current github page"""
    bot.say("https://github.com/situx/tuxbot")

@module.commands('snack')
@module.example('.snack')
def snack(bot, trigger):
    bot.say('Nomnomnom')

@module.commands('ping')
@module.example('.ping')
def helloworld(bot, trigger):
    bot.say('pong')

@module.commands('pong')
@module.example('.pong')
def pong(bot,trigger):
    bot.say('ping')

@module.commands('peng')
@module.example('.peng')
def peng(bot,trigger):
    bot.say('pong')

@module.commands('schnickschnackschnuck\s(schere|stein|papier)','schnick\s(schere|stein|papier)')
@module.example('.schnick stein','schnickschnackschnuck papier')
def schnickschnackschnuck(bot,trigger):
    """Plays the game rock, paper, scissors"""
    userinput=trigger.group(2).lower()
    switcher = {
                  0: "schere",
                  1: "stein",
                  2: "papier"
    }
    rand=randint(0,len(switcher)-1)
    botinput=switcher[rand]
    bot.say(trigger.nick+": "+userinput)
    bot.say(bot.nick+": "+botinput)
    if (botinput=="schere" and  userinput=="papier") or (botinput=="stein" and userinput=="schere") or (botinput=="papier" and userinput=="stein"):
        bot.say(bot.nick+": gewinnt!")
    elif (botinput=="schere" and userinput=="stein") or (botinput=="stein" and userinput=="papier") or (botinput=="papier" and userinput=="schere"):
        bot.say(trigger.nick+": gewinnt!")
    elif (botinput=="schere" and userinput=="schere") or (botinput=="stein" and userinput=="stein") or (botinput=="papier" and userinput=="papier"):
        bot.say("Unentschieden!")

       
@module.commands('schnickschnackschnuck2\s(schere|stein|papier|echse|spock)','schnick2\s(schere|stein|papier|echse|spock)')
@module.example('.schnick2 spock','.schnickschnackschnuck2 echse')
def schnickschnackschnuck(bot,trigger):
    """Plays the game stone, paper, scissors, lizard spock known from the series The Big Bang Theory"""
    userinput=trigger.group(2).lower()
    switcher = {
                  0: "schere",
                  1: "stein",
                  2: "papier",
                  3: "echse",
                  4: "spock"
    }
    rand=randint(0,len(switcher)-1)
    botinput=switcher[rand]
    bot.say(trigger.nick+": "+userinput)
    bot.say(bot.nick+": "+botinput)
    if (botinput=="schere" and  userinput=="papier") or (botinput=="schere" and userinput=="echse") or (botinput=="stein" and userinput=="schere") or (botinput=="stein" and userinput=="echse") or (botinput=="papier" and userinput=="stein") or (botinput=="echse" and userinput=="papier") or (botinput=="papier" and userinput=="spock") or (botinput=="echse" and userinput=="spock")  or (botinput=="spock" and userinput=="schere") or (botinput=="spock" and userinput=="stein") :
        bot.say(bot.nick+": gewinnt!")
    elif (botinput==userinput):
        bot.say("Unentschieden!")
    else:
        bot.say(trigger.nick+": gewinnt!")
