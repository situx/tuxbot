from sopel import web
from sopel.module import commands, example, NOLIMIT

import xmltodict
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
import re, cgi
import html.parser

tag_re=re.compile(r'(<!--.*?-->|<[^>]*>)')

@commands('randomquote', 'rq')
@example('.randomquote')
def randquote(bot,trigger):
    baseurl = "http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1"
    result = urllib.request.urlopen(baseurl).read()
    data = json.loads(result.decode())
    bot.say("\""+html.unescape(tag_re.sub('',data[0]['content']))+"\"")
    bot.say(html.unescape(data[0]['title']))#+" - "+data[0]['link'])
