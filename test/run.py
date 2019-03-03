import tool
from click.testing import CliRunner

class bcolors:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    purple = '\033[95m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'
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
runner = CliRunner()
result = runner.invoke(tool.runner, [f'--league {league} --standings'])
#main(league=league, time=time, standings=standings, team=team, live=live, use12hour=use12hour, players=players, output_format=output_format, output_file=output_file, upcoming=upcoming, lookup=lookup, listcodes=listcodes, apikey=apikey)