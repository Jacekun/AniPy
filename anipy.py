# imports
import os
import json
import requests
from datetime import datetime
import argparse
# Local Imports
import func.main as fMain
import func.anilist_request as fReq
from func.anilist_getMedia import getMediaEntries
import func.trim_list as fTrim
import func.getNotOnTachi as fNotOnTachi

# App Properties
appVersion = '1.11'
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) #os.path.dirname(sys.executable)
anilistConfig = "anilistConfig.json"
# Vars for Authentication
ANICLIENT = ""
ANISECRET = ""
useOAuth = False
# User vars
username = ""
userID = 0
# Output file names
outputAnime = []
outputManga = []
entryLog = os.path.join(PROJECT_PATH, "output", "entries.log") # Log entries

# Create 'output' directory
if not os.path.exists('output'):
    os.makedirs('output')

parser = argparse.ArgumentParser(description='AniPy parameters and flags')

# Required params
parser.add_argument('mal', type=str, help='MAL Username')
# Optional params
parser.add_argument('-user', type=str, help='Anilist Username, if using Public mode') # If using Public mode
parser.add_argument('-tachi', type=str, help='Tachiyomi legacy backup')
# Flags
parser.add_argument('--a', action='store_true', help='Use Authenticated mode')
parser.add_argument('--t', action='store_true', help='Trim generated files')

# Parse args
args = parser.parse_args()

if (args.a):
    fMain.logger("Authenticated mode!")
else:
    fMain.logger(f'Username: {args.user}')