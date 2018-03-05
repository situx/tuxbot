import xml.etree.ElementTree as ET
import sopel.module
from random import randint
import math
import random

insulthash={}
playerhash={}
piratenames=[]
counter=0
lang='de'

def setup(bot):
    e = ET.parse('/home/bananapi/.sopel/modules/monkeyphrases.xml').getroot()
    for atype in e.findall('pair'):
        if not atype.get('lang') in insulthash:
            insulthash[atype.get('lang')]={}
        insulthash[atype.get('lang')][atype.get('question')]=atype.get('answer')

@sopel.module.commands('fighten\s+(.*)')
@sopel.module.example('.fighten nick')
def fighten(bot,trigger):
    """Starts the insult sword fighting game in English for a given nick"""
    global lang
    lang='en'
    fightde(bot,trigger)

@sopel.module.commands('fightde\s+(.*)')
@sopel.module.example('.fightde nick')
def fightde(bot,trigger):
    """Starts the insult sword fighting game in German for a given nick"""
    global lang
    if lang=='':
        lang='de'
    if not trigger.nick in playerhash:
        counter=-1
        rand=randint(1,len(list(insulthash[lang].keys())))
        bot.say("Du trittst an gegen: Pirat auf Level "+str(math.ceil((float(rand)/float(len(insulthash[lang])))*100))+"%")
        bot.say("\00304[.."+trigger.nick+"/ \Pirat..]")
        bot.say("Arrgh! Du willst mich herausfordern?");
        bot.say("So sei es!")
        x=random.sample(list(range(0,len(list(insulthash[lang].keys())))), rand)
        playerhash[trigger.nick]={}
        playerhash[trigger.nick]['currentquestion']=list(insulthash[lang].keys())[x[counter+1]]
        playerhash[trigger.nick]['randhash']=x
        playerhash[trigger.nick]['counter']=counter
        playerhash[trigger.nick]['stat']=0
    else:
        counter=playerhash[trigger.nick]['counter']
        if insulthash[lang][playerhash[trigger.nick]['currentquestion']] in trigger.group(1):
            playerhash[trigger.nick]['stat']=playerhash[trigger.nick]['stat']+1
        else:
            playerhash[trigger.nick]['stat']=playerhash[trigger.nick]['stat']-1
        if playerhash[trigger.nick]['stat']>2:
            bot.say("Du hast gewonnen! Nimm meinen Schatz!")
            lang=''
            playerhash[trigger.nick]={}
            return
        elif playerhash[trigger.nick]['stat']<-2:
            lang=''
            bot.say("Du hast verloren! Gib mir deinen Schatz!")
            playerhash[trigger.nick]={}
            return
        elif playerhash[trigger.nick]['stat']==0:
            bot.say("\00304[.."+trigger.nick+"/ \Pirat..]")
        elif playerhash[trigger.nick]['stat']==1:
            bot.say("\00304[..."+trigger.nick+"/ \Pirat.]")
        elif playerhash[trigger.nick]['stat']==2:
            bot.say("\00304[...."+trigger.nick+"/ \Pirat]")
        elif playerhash[trigger.nick]['stat']==-1:
            bot.say("\00304[."+trigger.nick+"/ \Pirat...]")
        elif playerhash[trigger.nick]['stat']==-2:
            bot.say("\00304["+trigger.nick+"/ \Pirat....]")
    counter=counter+1
    randhash=playerhash[trigger.nick]['randhash']
    if counter>len(playerhash[trigger.nick]['randhash']):
        counter=0
    playerhash[trigger.nick]['currentquestion']=list(insulthash[lang].keys())[randhash[counter]]
    playerhash[trigger.nick]['counter']=counter
    bot.say("\002"+list(insulthash[lang].keys())[randhash[counter]])


#setup("")
#fightde("","")
