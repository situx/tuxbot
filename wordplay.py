import xml.etree.ElementTree as ET
import sopel.module

wordhash={}
credithash={}

def setup(bot):
    e = ET.parse('/home/bananapi/.sopel/modules/words.xml').getroot()
    for atype in e.findall('user'):
        wordhash[atype.get('name')]=float(atype.get('value'))
        credithash[atype.get('name')]=float(atype.get('credit'))


@sopel.module.commands('wortspielcredit')
def wortspielcredit(bot,trigger):
    if trigger.nick=="situx":
        for key in credithash:
            credithash[key]=float(10)
        bot.say("Der Wortspielkredit wurde auf 10 Euro zurueckgesetzt!")
    else:
        bot.say(trigger.nick+": Du bist nicht dazu berechtigt den Wortspielkredit zurueckzusetzen!")
    toxml()

@sopel.module.commands('wortspielreset')
def wortspielreset(bot,trigger):
    if trigger.nick=="situx":
        global wordhash
        global credithash
        wordhash={}
        credithash={}
        bot.say("Die Wortspielkasse wurde geleert!");
    else:
        bot.say(trigger.nick+": Du bist nicht dazu berechtigt die Wortspielkasse zu leeren!")
    toxml()

@sopel.module.commands('wortspiel\s+([A-z]+)\s+([0-9]+[\.|,]?[0-9]*)')
def helloworld(bot, trigger):
    payment=round(float(trigger.group(3)),2)
    if not trigger.group(2) in credithash:
        credithash[trigger.group(2)]=float(10)
    if not trigger.nick in credithash:
        credithash[trigger.nick]=float(10)
    if trigger.group(2)==bot.nick:
        bot.reply("Das haettest du wohl gerne!")
        return
    if credithash[trigger.nick]<payment:
        bot.say(trigger.nick+"("+str(credithash[trigger.nick])+") hat nicht mehr genuegend Euro")
        return
    else:
        if trigger.group(2) in wordhash:
            wordhash[trigger.group(2)]=wordhash[trigger.group(2)]+payment
        else:
            wordhash[trigger.group(2)]=payment
        bot.say(trigger.nick+"("+str(credithash[trigger.nick])+" Euro) befiehlt: "+trigger.group(2)+" zahlt "+str(payment)+" Euro in die Wortspielkasse!")
        credithash[trigger.nick]=credithash[trigger.nick]-payment
        bot.say(trigger.group(2)+" hat insgesamt "+str(wordhash[trigger.group(2)])+" Euro in die Wortspielkasse bezahlt")
        bot.say(trigger.nick+" hat noch "+str(credithash[trigger.nick])+"Euro")
        bot.say("In der Wortspielkasse sind nun: "+str(sum(wordhash.values()))+" Euro!")
        toxml()

@sopel.module.commands('wortspielstats')
def wordplaystat(bot,trigger):
    bot.say("Wortspielstatistik: ")
    for key in wordhash:
        bot.say(key+": "+str(wordhash[key])+" Euro")
    bot.say("Gesamt: "+str(sum(wordhash.values()))+" Euro")

@sopel.module.commands('creditstats')
def creditstat(bot,trigger):
    bot.say("Kreditstatistik: ")
    for key in credithash:
        bot.say(key+": "+str(credithash[key])+" Euro")
    bot.say("Gesamt: "+str(sum(credithash.values()))+" Euro")

def toxml():
    root = ET.Element('data')
    for key in wordhash:
        user=ET.SubElement(root,'user')
        user.set("name",key)
        user.set("value",str(wordhash[key]))
        user.set("credit",str(credithash[key]))
    tree=ET.ElementTree(root)
    tree.write('words.xml')
