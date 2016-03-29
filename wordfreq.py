import xml.etree.ElementTree as ET
import sopel.module
import operator

user={}

@sopel.module.rule('([^\.].*)')
def wordfreq(bot,trigger):
  if(trigger.nick!=bot.nick):
     message=trigger.group(1).replace("?","").replace("!","").replace(".","").replace(",","")
     words=message.split( )
     if not trigger.nick in user:
         user[trigger.nick]={}#
     for word in words:
         if not word in user[trigger.nick]:
             user[trigger.nick][word]=0
         user[trigger.nick][word]=user[trigger.nick][word]+1
         
@sopel.module.commands('wordfreq\s([A-z]+)\s?([0-9]+)?')
def wordfreqcom(bot,trigger):
    maxval=0
    maxkey=""
    if trigger.group(2) in user:
        resulthash={}
        for key in sorted(user[trigger.group(2)]):
            if not user[trigger.group(2)][key] in resulthash:
                resulthash[user[trigger.group(2)][key]]=""
            resulthash[user[trigger.group(2)][key]]+="'"+key+"'/ "
            if maxval<user[trigger.group(2)][key]:
                maxval=user[trigger.group(2)][key]
                maxkey=resulthash[user[trigger.group(2)][key]]
        keynumber=0
        if trigger.group(3):
         keynumber=int(trigger.group(3))
        if keynumber:
           newA = dict(sorted(resulthash.iteritems(), reverse=True)[:keynumber])
        else:
           newA = dict(sorted(resulthash.iteritems(), reverse=True)[:5])
           keynumber=5
       bot.say(trigger.group(2)+"'s "+str(keynumber)+" most used words  since this bot was started:")
        for key in sorted(newA.keys(),reverse=True):
         if key!=1:
            bot.say(str(newA[key]).strip().replace("/",",")+" ("+str(key)+" times used)")
    else:
      bot.say("No statistics for user "+trigger.group(2))

def toxml():
        root = ET.Element('data')
        for key in user:
                user=ET.SubElement(root,'user')
                user.set("name",key)
