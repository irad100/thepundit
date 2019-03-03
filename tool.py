import os
import sys
import json

import leagueids
from exceptions import IncorrectParametersException
from writers import get_writer
from request_handler import RequestHandler

colors = {'red': '\033[91m', 'green': '\033[92m', 'yellow': '\033[93m', 'blue': '\033[94m', 'purple': '\033[95m', 'bold': '\033[1m', 'underline': '\033[4m', 'end': '\033[0m'}

def load_json(file):
    """Load JSON file at app start"""
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, file)) as jfile:
        data = json.load(jfile)
    return data


LEAGUE_IDS = leagueids.LEAGUE_IDS
TEAM_DATA = load_json("teams.json")["teams"]
TEAM_NAMES = {team["code"]: team["id"] for team in TEAM_DATA}


def get_input_key():
    """Input API key and validate"""
    print(colors['yellow'] + colors['bold'] + "No API key found!" + colors['end'])
    print(colors['yellow'] + colors['bold'] + f"Please visit {RequestHandler.BASE_URL} and get an API token." + colors['end'])
    while True:
        confkey = input(colors['yellow'] + colors['bold'] + "Enter API key"+ colors['end'])
        if len(confkey) == 32:  # 32 chars
            try:
                int(confkey, 16)  # hexadecimal
            except ValueError:
                print(colors['red'] + colors['bold'] + "Invalid API key" + colors['end'])
            else:
                break
        else:
            print(colors['red'] + colors['bold'] + "Invalid API key" + colors['end'])
    return confkey


def load_config_key():
    """Load API key from config file, write if needed"""
    global api_token
    try:
        api_token = os.environ['SOCCER_CLI_API_TOKEN']
    except KeyError:
        home = os.path.expanduser("~")
        config = os.path.join(home, ".soccer-cli.ini")
        if not os.path.exists(config):
            with open(config, "w") as cfile:
                key = get_input_key()
                cfile.write(key)
        else:
            with open(config, "r") as cfile:
                key = cfile.read().splitlines()[0]
        if key:
            api_token = key
        else:
            os.remove(config)  # remove 0-byte file
            print('No API Token detected. '
                        'Please visit {0} and get an API Token, '
                        'which will be used by Soccer CLI '
                        'to get access to the data.'
                        .format(RequestHandler.BASE_URL), fg="red", bold=True)
            sys.exit(1)
    return api_token


def map_team_id(code):
    """Take in team ID, read JSON file to map ID to name"""
    for team in TEAM_DATA:
        if team["code"] == code:
            print(colors['green'] + team["name"] + colors['end'])
            break
    else:
        print(colors['red'] + colors['bold'] + "No team found for this code" + colors['end'])


def list_team_codes():
    """List team names in alphabetical order of team ID, per league."""
    # Sort teams by league, then alphabetical by code
    cleanlist = sorted(TEAM_DATA, key=lambda k: (k["league"]["name"], k["code"]))
    # Get league names
    leaguenames = sorted(list(set([team["league"]["name"] for team in cleanlist])))
    for league in leaguenames:
        teams = [team for team in cleanlist if team["league"]["name"] == league]
        print(colors['green'] + league + colors['end'])
        for team in teams:
            if team["code"] != "null":
                print(colors['yellow'] + colors['bold'] + f"{team['code']}: {team['name']}" + colors['end'])
    print("")


# String, Select fixtures from a particular league. League codes: WC: World Cup, EC: European Championship, CL: Champions League, PL: English Premier League, ELC: English Championship, FL1: French Ligue 1, BL: German Bundesliga, SA: Serie A, DED: Eredivisie, PPL: Primeira Liga, PD: Primera Division, BSA: Brazil Serie A
# league='PL'
# Integer, number of days in the past for which you want to see the scores, or the number of days in the future when used with --upcoming command.
# time=6 
# Boolean, Standings for a particular league.
# standings=True
# String, Choose a particular team's fixtures. Team codes: BAY, HSV, FCA, BSC, B04, TSG, DAR, H96, M05, FCI, SVW, S04, BVB, BMG, WOB, SGE, VFB, FCK, null, PFC, EVA, FCM, RCL, SUSFC, PSV, ROM, JUVE, PAL, GEN, SASS, SSC, LAZ, INT, FCT, FIO, ACM, EMP, KAI, EBS, SVS, SCF, FCN, FSV, RBL, GRE, KAR, HEI, 1860, PAD, VFL, FCP, FCU, FOR, MUFC, THFC, AFCB, AVFC, EFC, WAT, LCFC, SUN, NCFC, CRY, CFC, SWA, NUFC, SFC, AFC, WHU, SCFC, LFC, WBA, MCFC, MFF, ASTA, GSK, CSK, SHA, ZEN, DYK, MTA, OLA, DIN, AUE, VFR, OSC, PSG, MAR, SMC, NIC, MON, NAN, GUI, MHSC, SCB, REN, BOR, REI, TOU, ETI, OLY, LOR, CFE, UDA, CCF, LAC, RSS, ESP, FCG, ATM, RAY, VAL, MAL, SEV, BIL, FCB, MAD, LUD, VIG, BET, VCF, GCF, EIB, SCP, SLB
# team='MUFC'
# Boolean, Shows live scores from various leagues.
# live=False
# Boolean, Displays the time using 12 hour format instead of 24 (default).
# use12hour=False
# Boolean, Shows players for a particular team.
# players=False
# String, Define Output Format. Options: stdout, csv, json
# output_format='stdout'
# String, Save output to a file (only if csv or json option is provided). e.g: /Users/user/football/out.json
# output_file=None
# Boolean, Displays upcoming games when used with --time command.
# upcoming=False
# Boolean, Get full team name from team code when used with --team command.
# lookup=False
# Boolean, List all valid team code/team name pairs.
# listcodes=False
# String, API key to use.
# apikey='901186e638fd4baa999bb2c32f4ef7d5'
def run(league='PL', time=6, standings=True, team=None, live=False, use12hour=False, players=False, output_format='stdout', output_file=None, upcoming=False, lookup=False, listcodes=False, apikey=None):
    """
    A CLI for live and past football scores from various football leagues.

    League codes:

    \b
    - WC: World Cup
    - EC: European Championship
    - CL: Champions League
    - PL: English Premier League
    - ELC: English Championship
    - FL1: French Ligue 1
    - BL: German Bundesliga
    - SA: Serie A
    - DED: Eredivisie
    - PPL: Primeira Liga
    - PD: Primera Division
    - BSA: Brazil Serie A
    """
    if not apikey:
        apikey = load_config_key()
    headers = {'X-Auth-Token': apikey}

    try:
        if output_format == 'stdout' and output_file:
            raise IncorrectParametersException('Printing output to stdout and '
                                               'saving to a file are mutually exclusive')
        writer = get_writer(output_format, output_file)
        rh = RequestHandler(headers, LEAGUE_IDS, TEAM_NAMES, writer)

        if listcodes:
            list_team_codes()
            return

        if live:
            rh.get_live_scores(use12hour)
            return

        if standings:
            if not league:
                raise IncorrectParametersException('Please specify a league. '
                                                   'Example --standings --league=PL')
            if league == 'CL':
                raise IncorrectParametersException('Standings for CL - '
                                                   'Champions League not supported')
            rh.get_standings(league)
            return

        if team:
            if lookup:
                map_team_id(team)
                return
            if players:
                rh.get_team_players(team)
                return
            else:
                rh.get_team_scores(team, time, upcoming, use12hour)
                return

        rh.get_league_scores(league, time, upcoming, use12hour)
    except IncorrectParametersException as e:
        print(colors['red'] + colors['bold'] + str(e) + colors['end'])


if __name__ == '__main__':
    run()
