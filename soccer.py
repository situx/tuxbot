#import soccer
#from soccer import main
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
import re
from sopel.module import commands, example
import itertools
#from soccer import leagueids
#from soccer.exceptions import IncorrectParametersException, APIErrorException
#from soccer.writers import get_writer


BASE_URL = 'http://api.football-data.org/alpha/'
LIVE_URL = 'http://soccer-cli.appspot.com/'
#LEAGUE_IDS = leagueids.LEAGUE_IDS
#TEAM_NAMES = teamnames.team_names
LEAGUE_IDS = {
    "BL": 394,
    "BL2": 395,
    "BL3": 403,
    "FL": 396,
    "FL2": 397,
    "EPL": 398,
    "EL1": 425,
    "LLIGA": 399,
    "SD": 400,
    "SA": 401,
    "PPL": 402,
    "DED": 404,
    "CL": 405
}

team_names = {
    "null": "532",
    "SWA": "72",
    "TSG": "2",
    "GUI": "538",
    "CRY": "354",
    "NAN": "543",
    "VFB": "10",
    "ACM": "98",
    "PSG": "524",
    "LOR": "525",
    "EIB": "278",
    "AVFC": "58",
    "EMP": "445",
    "ESP": "80",
    "WBA": "74",
    "LAC": "560",
    "PAL": "114",
    "LAZ": "110",
    "SEV": "559",
    "AFCB": "1044",
    "ETI": "527",
    "JUVE": "109",
    "BMG": "18",
    "LFC": "64",
    "WHU": "563",
    "EFFZEH": "1",
    "SMC": "514",
    "GCF": "83",
    "SCB": "536",
    "FCT": "586",
    "FCA": "16",
    "FCB": "81",
    "M05": "15",
    "HSV": "7",
    "DAR": "55",
    "SUN": "71",
    "FCI": "31",
    "OSC": "521",
    "SGE": "19",
    "BOR": "526",
    "BSC": "9",
    "ATM": "78",
    "NUFC": "67",
    "VCF": "94",
    "VALL": "87",
    "THFC": "73",
    "FCG": "82",
    "BIL": "77",
    "TOU": "511",
    "AFC": "57",
    "ROM": "100",
    "OLY": "523",
    "SASS": "471",
    "B04": "3",
    "H96": "8",
    "Watfordfc": "346",
    "SVW": "12",
    "MON": "518",
    "EFC": "62",
    "FIO": "99",
    "LCFC": "338",
    "WOB": "11",
    "MAR": "516",
    "VIG": "558",
    "REN": "529",
    "Int": "108",
    "NIC": "522",
    "S04": "6",
    "CFC": "61",
    "MAL": "84",
    "NCFC": "68",
    "BVB": "4",
    "REI": "547",
    "MAD": "86",
    "LUD": "88",
    "MUFC": "66",
    "MCFC": "65",
    "SCFC": "70",
    "VAL": "95",
    "SFC": "340",
    "SSC": "113",
    "RSS": "92",
    "BM": "5",
}

@commands('soccerlive')
def soccerlive(bot,trigger):
    scores=json.loads(urllib.request.urlopen(LIVE_URL).read().decode())
    if len(scores["games"]) == 0:
            bot.say("No live action currently")
            return
    scoressorted=sorted(scores["games"],key=lambda x:x["league"])
    for league,games in itertools.groupby(scoressorted,key=lambda x: x["league"]):
        bot.say(league)
        for game in games:
            if 'result' in game:
                bot.say(game["result"]["homeTeamName"]+"\t"+str(game["result"]["goalsHomeTeam"])+"  vs "+str(game["result"]["goalsAwayTeam"])+" "+game["result"]["awayTeamName"])
            else:
                bot.say(game["homeTeamName"]+"\tvs \t"+game["awayTeamName"])

@commands('soccerteams')
def soccerteams(bot,trigger):
    list_team_codes(bot)

@commands('soccertable\s([A-Z]+[0-9]?)')
def soccertable(bot,trigger):
    leagueid=LEAGUE_IDS[trigger.group(2)]
    table=json.loads(urllib.request.urlopen(BASE_URL+"soccerseasons/"+str(leagueid)+"/leagueTable").read().decode())
    clubnamelength=""
    for team in table["standing"]:
        if len(clubnamelength)<len(team["teamName"]):
            clubnamelength=team["teamName"]
    print(clubnamelength+" "+str(len(clubnamelength)))
    clubnamelength=re.sub('.',' ',clubnamelength)
    bot.say("POS\tCLUB"+clubnamelength[0:len(clubnamelength)-4]+"\tPLAYED\tGOAL DIFF\tPOINTS")
    for team in table["standing"]:
        print(team["teamName"]+" "+str(len(clubnamelength)-len(team["teamName"])))
        bot.say(str(team["position"])+"\t"+str(team["teamName"])+clubnamelength[0:len(clubnamelength)-len(team["teamName"])]+"\t"+str(team["playedGames"])+"\t"+str(team["goalDifference"])+"\t"+str(team["points"]))

def list_team_codes(bot):
    """List team names in alphabetical order of team ID."""
    teamcodes = sorted(TEAM_NAMES.keys())
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "teamcodes.json")) as jfile:
        data = json.load(jfile)
    for code in teamcodes:
        for key, value in data.iteritems():
            if value == code:
                bot.say(u"{0}: {1}".format(value, key))
                break
