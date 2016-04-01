from sopel.module import commands, example, NOLIMIT
import urllib.request, urllib.parse, urllib.error
import json
import re
import time

areas =["North","South","East","West","Central"]
url = 'http://www.nea.gov.sg/anti-pollution-radiation-protection/air-pollution-control/psi/psi-readings-over-the-last-24-hours'
cache_duration= 60 * 30
cached_psi={}
cached_time=None
chosen_area=None

@commands('sghaze','sghaze\s+(north|south|east|west|central)')
def sghaze(bot,trigger):
        global chosen_area
        chosen_area=trigger.group(2)
        result=cachedd_psi()
        if chosen_area:
                chosen_area=chosen_area.capitalize()
                bot.say("Air Quality Index for Singapore "+chosen_area+" district: ")
        else:
                bot.say("Air Quality Index for Singapore:")
        for key in result:
                bot.say(key+": "+rate_result(cached_psi[key]))

@commands('sghazeinfo')
def sghazelegend(bot,trigger):
        bot.say('Air Quality Index Info:')
        bot.say('0-50: None')
        bot.say('51-100: Moderate')
        bot.say('101-200: Unhealthy')
        bot.say('201-300: Very Unhealthy')
        bot.say('301-400: Hazardous')
        bot.say('>400 Beyond Hazardous')
        bot.say('More information: https://en.wikipedia.org/wiki/Air_quality_index')

def rate_result(resnumber):
        if resnumber<=50:
                return"None ("+str(resnumber)+")"
        if resnumber>50 and resnumber<=100:
                return "Moderate ("+str(resnumber)+")"
        if resnumber>100 and resnumber<=200:
                return "Unhealthy ("+str(resnumber)+")"
        if resnumber>200 and resnumber<=300:
                return "Very Unhealthy ("+str(resnumber)+")"
        if resnumber>300 and resnumber<=400:
                return "Hazardous ("+str(resnumber)+")"
        if resnumber>400:
                return "Beyond Hazardous ("+str(renumber)+")"

def cachedd_psi():
        time_now=time.time()
        global cached_psi
        global cached_time
        if cached_psi and cached_time and not time_now-cached_time>cached_duration:
                return cached_psi
        cached_psi=get_psi()
        cache_time=time.time()
        return cached_psi

def get_psi():
        global chosen_area
        psi={}
        html=urllib.request.urlopen(url).read().decode()
        #print(html)
        if chosen_area:
                m = re.search('<strong>'+chosen_area+'<\/strong>.*?<strong[^>]+>(\d+)',html,re.M|re.S)
                if m:
                        psi[chosen_area]=int(m.group(1))
        else:
                for area in areas: 
                        #print(area)
                        m = re.search('<strong>'+area+'<\/strong>.*?<strong[^>]+>(\d+)',html,re.M|re.S)
                        #print(m)
                        if m:
                                psi[area]=int(m.group(1))
        return psi
