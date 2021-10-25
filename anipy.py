# imports
import os
import requests
import argparse
# Local Imports
import func.main as fMain
import func.anilist_request as fReq
from func.anilist_getMedia import getMediaEntries
import func.trim_list as fTrim
import func.getNotOnTachi as fNotOnTachi

# App Properties
appVersion = '1.13'
appMode = 'AniPy (Advanced)'
# Declare variables
fMain.logger("Define Filepaths..")
# Paths for Files
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) #os.path.dirname(sys.executable)
fMain.logger("Current path: " + PROJECT_PATH)
# Filepaths
anilistConfig = os.path.join(PROJECT_PATH, "anilistConfig.json")
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

# Vars for Authentication
ANICLIENT = ""
ANISECRET = ""
useOAuth = False
accessToken = ""
# User vars
username = args.mal # Required. MAL Username
userID = 0
anilistUser = None
# Output file names
outputAnime = []
outputManga = []

if args.user is not None:
    anilistUser = str(args.user)

# use same MAL username if none
if anilistUser is None:
    anilistUser = str(username)

if (args.a):
    useOAuth, ANICLIENT, ANISECRET, REDIRECT_URL = fReq.setup_config(anilistConfig)

    if not useOAuth:
      accessToken = ""
    
    if useOAuth:
      code = fReq.request_pubcode(ANICLIENT, REDIRECT_URL)
      accessToken = fReq.request_accesstkn(ANICLIENT, ANISECRET, REDIRECT_URL, code)

    if accessToken:
      useOAuth = True
      fMain.logger("Has access token!")
    else:
      useOAuth = False
      fMain.logger("Cannot Authenticate! Will use Public List.")
    
# Check whether authenticated, or use public Username
if not useOAuth:
    fMain.logger("'Public Username' Mode")
    accessToken = ""
    userID = fReq.anilist_getUserID(anilistUser) # Fetch UserID using username
else:
    fMain.logger("Getting User ID, from Authenticated user..")
    userID = fReq.anilist_getUserID_auth(accessToken)

if userID is not None:
    if (userID < 1):
        fMain.logger(f'Invalid user ID: {userID}!')
else:
    fMain.logger("User Id cannot be fetched!")

# Display User ID
fMain.logger("User ID: " + str(userID))

# Delete prev files
fMain.deleteFile(entryLog)

# Request anime list
outputAnime = getMediaEntries("ANIME", accessToken, userID, username, PROJECT_PATH, entryLog, useOAuth)

# Request manga list
outputManga = getMediaEntries("MANGA", accessToken, userID, username, PROJECT_PATH, entryLog, useOAuth)

# Trim List
if args.t:
    fTrim.trim_results(PROJECT_PATH, outputAnime.get('main'), outputManga.get('main'), False)
    fTrim.trim_results(PROJECT_PATH, outputAnime.get('nsfw'), outputManga.get('nsfw'), True)

# Get Entries not on Tachi
tempTachi = str(args.tachi)
if tempTachi:
    fNotOnTachi.getNotOnTachi(outputManga.get('main'), tempTachi, False)
    fNotOnTachi.getNotOnTachi(outputManga.get('nsfw'), tempTachi, True)

fMain.inputX("Press <Enter> to exit..")