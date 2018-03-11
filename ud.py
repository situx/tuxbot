'''
Module for doing queries on urbandictionary
'''

import json

from sopel import web
from sopel.module import commands

UD_URL = 'http://api.urbandictionary.com/v0/'


def get_def(path, num=0):
    url = UD_URL + path
    try:
        resp = json.loads(web.get(url))
    except UnicodeError:
        definition = ('ENGLISH MOTHERFUCKER, DO YOU SPEAK IT?')
        return definition
    nom = num + 1
    try:
        word = path[12:]
    except:
        pass
    if path.startswith("define?term=") and resp['result_type'] == 'no_results':
        definition = 'Definition %s not found!' % (word)
    else:
        try:
            item = resp['list'][num]['definition'].encode('utf8')
            thumbsup = resp['list'][num]['thumbs_up']
            thumbsdown = resp['list'][num]['thumbs_down']
            points = str(int(thumbsup) - int(thumbsdown))
            total_nom = len(resp['list'])
            word = resp['list'][num]['word'].encode('utf8')
            definition = str(word)[1:] + ": " + str(item)[1:] + " | Number: " + str(nom) + '/' + str(total_nom) + ' | Points: ' + points + ' (03' + str(thumbsup) + '|05' + str(thumbsdown) + ')'
        except IndexError:
            definition = ('Definition entry %s does'
                          'not exist for \'%s\'.' % (nom, word))
    return format_string(definition)


def format_string(definition):
    definition = definition.replace('\\r\\n', ' ')
    definition = definition.replace('\\n', ' ')
    definition = definition.replace('\\r', '')
    definition = definition.replace('\n', ' ')
    definition = definition.replace('\r', '')
    definition = definition.replace("\\'", "'")
    definition = definition.strip()
    return definition


@commands('urban')
def urban(bot, trigger):
    defnum = 0
    if not trigger.group(2):
        path = "random"
    else:
        args = trigger.group(2).replace(', ', ',').split(',')
        word = ' '.join(args)
        if len(args) > 1:
            try:
                defnum = int(args[0])
                defnum = defnum - 1
                word = ' '.join(args[1:])
            except ValueError:
                pass
        path = "define?term=" + word
    definition = get_def(path, defnum)
    bot.say(definition, max_messages=3)
