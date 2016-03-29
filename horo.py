import urllib.request, urllib.error, urllib.parse
import sopel.module
import json
import time

germanmatch={"Wassermann":"aquarius","Fische":"pisces","Widder":"aries","Stier":"taurus","Zwillinge":"gemini","Krebs":"cancer","Loewe":"lion","Jungfrau":"virgin","Waage":"libra","Skorpion":"scorpio","Schuetze":"sagittarius","Steinbock":"capricorn"}

@sopel.module.commands('horo[scope]?\s+(.+)')
#@sopel.module.example('.horo scorpio')
def forecast(bot,trigger):
    zsign=trigger.group(2)
    if trigger.group(2) in germanmatch:
        zsign=germanmatch[trigger.group(2)]
    baseurl = "http://widgets.fabulously40.com/horoscope.json?sign="+zsign
    #print(baseurl)
    result = urllib.request.urlopen(baseurl).read()
    #bot.say(baseurl)
    data = json.loads(result)
    #bot.say(str(data))
    if not "horoscope" in data:
        bot.say("I do not know this zodiac sign!")
    else:
        bot.say("Horoscope for "+data["horoscope"]["sign"]+" "+time.strftime("%d.%m.%Y")+":")
        bot.say(data["horoscope"]["horoscope"])
