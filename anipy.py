# imports
import os
import argparse
# Local Imports
import func.main as fMain
import func.anilist_request as fReq
from func.anilist_getMedia import getMediaEntries
import func.trim_list as fTrim
import func.getNotOnTachi as fNotOnTachi

# App Properties
appVersion = '1.20'
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
parser.add_argument('--n', action='store_true', help='Separate NSFW entries on output files')

# Parse args
args = parser.parse_args()

# Vars for Authentication
ANICLIENT = ""
ANISECRET = ""
useOAuth = False
accessToken = ""
# User vars
username = str(args.mal) # Required. MAL Username
userID = 0
anilistUser = None
isSepNsfw = False # Separate nsfw entries on output
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

# Separate NSFW Entries
if (args.n):
    isSepNsfw = True

# Delete prev files
fMain.deleteFile(entryLog)

# Initiate parameter values
paramvals = {
    'root': PROJECT_PATH,
    'log': entryLog,
    'access_tkn': accessToken,
    'user_id': userID,
    'username': username,
    'use_auth': useOAuth,
    'sep_nsfw': isSepNsfw
}

# Request anime list
outputAnime = getMediaEntries("ANIME", paramvals)

# Request manga list
outputManga = getMediaEntries("MANGA", paramvals)

# Trim List
if args.t:
    fTrim.trim_results(PROJECT_PATH, outputAnime.get('main'), outputManga.get('main'), False)
    if isSepNsfw:
        fTrim.trim_results(PROJECT_PATH, outputAnime.get('nsfw'), outputManga.get('nsfw'), True)

# Get Entries not on Tachi
tempTachi = str(args.tachi)
if tempTachi:
    fNotOnTachi.getNotOnTachi(outputManga.get('main'), tempTachi, False)
    if isSepNsfw:
        fNotOnTachi.getNotOnTachi(outputManga.get('nsfw'), tempTachi, True)

fMain.inputX("Press <Enter> to exit..", "")
