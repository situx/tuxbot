import feedparser
from sopel.module import commands, example, NOLIMIT

@commands('fefe')
def getfefefeed(bot,trigger):
    d = feedparser.parse('https://blog.fefe.de/rss.xml')
    bot.say(d['feed']['title'])
    for entry in ['entries']:
        bot.say(entry)

d = feedparser.parse('http://blog.fefe.de/rss.xml?html')
print(d['feed']['title'])
print(d['feed'])

