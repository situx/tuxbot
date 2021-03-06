from sopel import web
from sopel.module import commands, example, NOLIMIT

import xmltodict
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
import re, cgi
import html.parser
import wikiquote
import random

tag_re=re.compile(r'(<!--.*?-->|<[^>]*>)')

@commands('randomquote', 'rq')
@example('.randomquote','rq')
def randquote(bot,trigger):
    """Gets a randomized quote"""
    baseurl = "http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1"
    result = urllib.request.urlopen(baseurl).read()
    data = json.loads(result.decode())
    bot.say("\""+html.unescape(tag_re.sub('',data[0]['content']))+"\"")
    bot.say(html.unescape(data[0]['title']))#+" - "+data[0]['link'])

@commands('quoteofday','qod')
@example('.quoteofday','qod')
def quoteofday(bot,trigger):
    """Retrieves a quote of day"""
    quoteofday=wikiquote.quote_of_the_day()
    bot.say(quoteofday[0])
    bot.say(quoteofday[1])    

@commands('quote\s([A-z0-9-\.\s]+)')
@example('quote Einstein')
def quoteofperson(bot,trigger):
    """Retrieves a quote from the person given as parameter"""
    result=wikiquote.quotes(trigger.group(2))
    if"NoSuchPageException" in result:
        bot.say("Not quote for person "+trigger.group(2)+" found!")
    else:
        bot.say(str(random.choice(wikiquote.quotes(trigger.group(2)))))


