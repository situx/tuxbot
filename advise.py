import xml.etree.ElementTree as ET
import sopel.module

advices={}

def setup(bot):
    e = ET.parse('/home/bananapi/.sopel/modules/advices.xml').getroot()
    for atype in e.findall('advice'):
        advices[atype.get('advicekey')]=str(atype.get('advicevalue'))


@sopel.module.commands('advice\s+([A-z]+)\s+([A-z]+)')
def advice(bot,trigger):
	adKey = trigger.group(3)
	targetNick = trigger.group(2)

    if targetNick==bot.nick:
        bot.reply("Das haettest du wohl gerne!")
        return

	if adKey in advices:
		bot.say(str(trigger.group(2)) + ": " + advices[adKey])
	else:
        bot.say("Ich habe keinen Rat mit dem Schluesselwort " + str(trigger.group(3)) + ". Momentan beherrsche ich " + str(len(advices)) + " Ratschlaege")

