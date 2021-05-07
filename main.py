# imports
import os
import importlib
import json
import requests
from datetime import datetime
import webbrowser

# App Properties
appVersion = '1.06'
appBuild = 2 # Used for building executable file

# Logger
def logger(text):
    print(f'[{datetime.now().strftime("%H:%M:%S")}][main]: {text}')

# Import config for Anilist OAuth
logger("Importing config")
with open('anilistConfig.json') as f:
  configData = json.load(f)
ANICLIENT = configData['aniclient']
ANISECRET = configData['anisecret']
REDIRECT_URL = configData['redirectUrl']
# logger("\nClient: " + ANICLIENT + "\nSecret: " + ANISECRET)

# Import libs from 'func'
logger("Importing scripts from same folder")
fMain = importlib.import_module("func.main")
fReq = importlib.import_module("func.anilist_request")
fGetAnime = importlib.import_module("func.anilist_getAnime")
fGetManga = importlib.import_module("func.anilist_getManga")
fTrim = importlib.import_module("func.trim_list")
fNotOnTachi = importlib.import_module("func.getNotOnTachi")

# Declare variables
logger("Define Global Vars..")
# Paths for Files
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) #os.path.dirname(sys.executable)
logger("Current path: " + PROJECT_PATH)

# Variables
inputChoice = input("Type '1' to skip oAuth (use Public), otherwise '0': ")

# Vars for Authentication
useOAuth = False
# User vars
username = ""
userID = 0
# Output file names
outputAnime = ""
outputManga = ""
entryLog = os.path.join(PROJECT_PATH, "output\\entries.log") # Log entries
# Trim List Output
outputAnimeTrim = ""
outputMangaTrim = ""

# json objects
jsonAnime = None
# List of IDs, to prevent duplicates
entryID = []

if inputChoice == '1':
  useOAuth = False
else:
  # Get OAuth and Access Token
  logger("Login Anilist on browser, and Authorize AniPy")
  url = f"https://anilist.co/api/v2/oauth/authorize?client_id={ANICLIENT}&redirect_uri={REDIRECT_URL}&response_type=code"
  webbrowser.open(url)

  code = input("Paste your token code here (Copied from Anilist webpage result): ")

  body = {
      'grant_type': 'authorization_code',
      'client_id': ANICLIENT,
      'client_secret': ANISECRET,
      'redirect_uri': REDIRECT_URL,
      'code': code
  }
  logger("Getting access token..")
  accessToken = requests.post("https://anilist.co/api/v2/oauth/token", json=body).json().get("access_token")
  #logger("Access Token: [" + accessToken + "]")
  if accessToken:
    useOAuth = True
    logger("Has access token!")
  else:
    useOAuth = False
    logger("Cannot Authenticate! Will use Public Username.")


# Check whether authenticated, or use public Username
if not useOAuth:
  logger("'Public Username' Mode")
  accessToken = ""
  while (userID < 1):
    # Get Username
    username = input("Enter your Anilist Username: ")
    userID = fReq.anilist_getUserID(username)
else:
  logger("Getting User ID, from Authenticated user..")
  resultUserID = requests.post("https://graphql.anilist.co", headers={"Authorization": f"Bearer {accessToken}"}, json={"query": "{Viewer{id}}"}).json()
  userID = resultUserID["data"]["Viewer"]["id"]
  logger("User ID: " + str(userID))

# Delete prev files
fMain.deleteFile(entryLog)

# Request anime list
fMain.write_append(entryLog, f'ANIME [{datetime.now().strftime("%Y-%m-%d")} {datetime.now().strftime("%H:%M:%S")}]\n')
outputAnime = fGetAnime.getAnimeEntries(accessToken, userID, username, PROJECT_PATH, entryLog, useOAuth)

# Request manga list
fMain.write_append(entryLog, f'MANGA [{datetime.now().strftime("%Y-%m-%d")} {datetime.now().strftime("%H:%M:%S")}]\n')
outputManga = fGetManga.getMangaEntries(accessToken, userID, username, PROJECT_PATH, entryLog, useOAuth)

# Trim List
fTrim.trim_results(PROJECT_PATH, outputAnime, outputManga)

# Get Entries not on Tachi
tempTachi = input("Tachiyomi library json file: ")
if tempTachi:
  fNotOnTachi.getNotOnTachi(outputManga, tempTachi)

input("Press <Enter> to exit..")