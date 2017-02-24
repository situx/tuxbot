#Event day plugin for tuxbot, modified from a birthday plugin
from datetime import datetime                                                                                                                                                         
import json                                                                                                                                                                           
import sopel                                                                                                                                                                          
import operator                                                                                                                                                                       
from collections import OrderedDict
from operator import itemgetter

globaldict={}

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def date_hook(json_dict):
    for(key, value) in json_dict.items():
        try:
            json_dict[key]["date"] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            pass
    return json_dict

def writejson(dict):
    with open('evday.json', 'w') as bdayfile:
        json.dump(dict, bdayfile, default=date_handler)

def readjson():
    with open('evday.json','r') as bdayfile:
        dict = json.loads(bdayfile.read(), object_hook=date_hook)
    return dict

def datetonext(dict):
    res = []
    today = datetime.today()
    for x,y in dict.items():
        delta = dict[x]["date"].replace(year=(datetime.today().year)) - today
        if delta.total_seconds() < 0:
            delta = dict[x]["date"].replace(year=(datetime.today().year+1)) - today
        res.append([x,delta])
    res.sort(key=lambda x: x[1])
    return res

def setbday(bot, trigger):
    #disabled function
    dict = readjson()
    name = trigger.nick
    try:
        date = datetime.strptime(trigger.group(1), '%m-%d')
    except:
        return bot.say("Please enter a valid date.  Accepts MONTH-DAY only.")
    dict[name]["date"] = date
    writejson(dict)
    bot.say("Event saved.")
#setbday.rule = r'^.setbday (\d{1,2}-\d{1,2})$'


@sopel.module.commands('evday','eventday')
def nextbday(bot, trigger):
    dict = readjson()
    res = datetonext(dict)
    if trigger.group(2):
        user = (trigger.group(2)).lower()
        try:
            bot.say("{0} is on {1}".format(user, dict[user].strftime("%B %d")))
        except:
            bot.say("Name not found...")
    else:
        btoday = 0
        for c in dict.items():
            if c[1].date() == datetime.today().replace(year=1904).date():
                btoday = "Today is {0} !".format(c[0])
        nname=res[0][0]
        nbday=(dict[nname]).strftime('%B %d')
        daysaway=(res[0][1]).days + 1
        if btoday:
            bot.say("{0} - Next event: {1} on {2} ({3} days away)".format(btoday, nname, nbday, daysaway))
        else:
            bot.say("Next event: {0} on {1} ({2} days away)".format(nname, nbday, daysaway))


@sopel.module.commands('addev\s([0-9A-z ,-]+)\s(1[0-2]|[1-9])\.([1-9]|1[012])\.?\s?(onetime)?\s?(.)?(.+)?','addevent\s([0-9A-z ,-]+)\s(1[0-2]|[1-9])\.([1-9]|1[012])\.?\s?(onetime)?\s?(.+)?')
def addbday(bot,trigger):
    dict=readjson()
    month=trigger.group(4)
    if len(month)<2:
        month="0"+month
    if trigger.group(1) in dict:
        bot.say("Event "+trigger.group(2)+" already exists!")
    else:
        dict[trigger.group(2)]={}
        dict[trigger.group(2)]["date"]="1970-"+month+"-"+trigger.group(3)+"T00:00:00"
        if trigger.group(5):
            dict[trigger.group(2)] ["onetime"]="true"
        else:
            dict[trigger.group(2)]["onetime"]="false"
        if trigger.group(6) and "http" in trigger.group(6):
            dict[trigger.group(2)]["url"]=trigger.group(6)
        else:
            dict[trigger.group(2)]["url"]=""
        writejson(dict)
        bot.say("Event "+trigger.group(2)+"("+trigger.group(3)+"."+trigger.group(4)+".) "+("(One Time Event)"if dict[trigger.group(2)]["onetime"]=="true" else "")+" successfully registered!")

@sopel.module.commands('remev\s([0-9A-z ,-]+)','removeevent\s([0-9A-z ,-]+)')
def removebday(bot,trigger):
    dict=readjson()
    if trigger.group(2) in dict:
        del dict[trigger.group(2)]
        writejson(dict)
        bot.say("Event "+trigger.group(2)+" deleted!")
    else:
        bot.say("No such event "+trigger.group(1))

@sopel.module.commands('evlist')
def bdaylist(bot,trigger):
    dictt=readjson()
    bot.reply("I am sending you the event list in a private message!")
    d = OrderedDict(sorted(dictt.items(), key=lambda x:x[1]["date"]))
    for key,val in d.items():
#        bot.say(key+" - "+str(val))
        bot.say(key+" - "+str(datetime.strptime(val["date"],"%Y-%m-%dT%H:%M:%S").day)+"."+str(datetime.strptime(val["date"],"%Y-%m-%dT%H:%M:%S").month)+". "+("(One Time Event)" if d[key]["onetime"]=="true" else ""),trigger.nick)


def gettodaysevents(dict):
    result=[]
    for key,val in dict.items():
        if dict[key]["date"].month== datetime.today().month and dict[key]["date"].day==datetime.today().day:
            result.append(key)
        if dict[key]["date"]== datetime.today()-datetime.timedelta(days=1) and dict[key]["onetime"]=="true":
            del dict[key]
    return result

@sopel.module.interval(21600)
def announce_bday(bot):
    #bot.say("Interval time")
    announce = []
    dict = readjson()
    res = gettodaysevents(dict)
    if len(res)>0:
        for chan in bot.channels:
            if len(res)>1:
                bot.say("Today's Events: {0}!".format(", ".join(res)),chan)
            else:
                bot.say("Today's Event: {0}!".format(",".join(res)),chan)
    writejson(dict)
#    else:
#        bot.msg("No events today!")
