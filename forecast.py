from sopel import web
from sopel.module import commands, example, NOLIMIT

import xmltodict
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json

@commands('forecast', 'fc')
@example('.forecast London')
def forecast(bot,trigger):
        location=trigger.group(2)
        woeid = ''
        result={}
        if not location:
            return bot.msg(trigger.sender, "I don't know where you live. " +
                           'Give me a location, like .forecast London, or tell me where you live by saying .setlocation London, for example.')
        else:
            location = location.strip()
            result=forecastsearch(location)
        if not result:
                return bot.reply("I don't know where that is.")
        data = result
        bot.say(data['channel']['title']+" "+data['channel']['item']['pubDate'])
        for dat in  data['channel']['item']['forecast'][:5]:
                bot.say(dat['day']+" "+dat['date']+" "+dat['text']+" "+dat['low']+"/"+dat['high']+"C")

def forecastsearch(query):
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = 'select * from geo.places where text="'+query+'"'
    yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
    print(yql_url)
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result.decode())
    #print(data['query']['results'])
    if not 'results' in data['query']:
        return
    places=data['query']['results']['place']
    for place in places:
        #print(place)
        if'woeid'==place or 'woeid' in place:
            if 'woeid'==place:
                woid=places['woeid']
            else:
                woid=place['woeid']
            #print(place['woeid'])
            baseurl="https://query.yahooapis.com/v1/public/yql?"
            yql_query="select * from weather.forecast where u='c' and woeid="+woid
            yql_url=baseurl+urllib.parse.urlencode({'q':yql_query})+"&format=json"
            print(yql_url)
            result=urllib.request.urlopen(yql_url).read()
            data=json.loads(result.decode())
            print()
            if 'results' in data['query']  and data['query']['results']!=None:
                print(data['query']['results'])
                return data['query']['results']
#   if not 'woeid' in data['query']['results']['place']:
#           woid=data['query']['results']['place'][0]['woeid']
 #  else:
  #         woid=data['query']['results']['place']['woeid']
   #if not woid:
#           return
#   print(woid)
#   baseurl = "https://query.yahooapis.com/v1/public/yql?"
#   yql_query = "select * from weather.forecast where u='c' and woeid="+woid
#   yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
#   print(yql_url)
#   result = urllib.request.urlopen(yql_url).read()
#   data = json.loads(result.decode())
#   print(data)
#   return data['query']['results']
    return

#forecastsearch("Hong Kong")
