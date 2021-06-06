# imports
import os
import json
import requests
from datetime import datetime
import webbrowser
# Local Imports
import func.main as fMain
import func.anilist_request as fReq
from func.anilist_getMedia import getMediaEntries
import func.trim_list as fTrim
import func.getNotOnTachi as fNotOnTachi

# App Properties
appVersion = '1.1'

# Logger
def logger(text):
    print(f'[{datetime.now().strftime("%H:%M:%S")}][main]: {text}')
def inputX(text):
  try:
    return input(f'[{datetime.now().strftime("%H:%M:%S")}][main]: {text}')
  except:
    return ""

# Declare variables
logger("Define Global Vars..")
# Paths for Files
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) #os.path.dirname(sys.executable)
logger("Current path: " + PROJECT_PATH)
anilistConfig = "anilistConfig.json"

# Vars for Authentication
ANICLIENT = ""
ANISECRET = ""
useOAuth = False
# User vars
username = ""
userID = 0
# Output file names
outputAnime = ""
outputManga = ""
entryLog = os.path.join(PROJECT_PATH, "output", "entries.log") # Log entries

# Create 'output' directory
if not os.path.exists('output'):
    os.makedirs('output')

# Toggle when skipping Public mode, or Authenticated mode
inputChoice = inputX("Type 'yes' or 'y' to Use Authenticated mode: ")
if not inputChoice:
  inputChoice = "n"

if inputChoice.lower()[0] == "y":
  # Import config for Anilist OAuth
  logger("Importing Anilist config")
  if not os.path.exists(anilistConfig):
    while not ANICLIENT:
      ANICLIENT = inputX("Enter your Client ID: ")
    while not ANISECRET:
      ANISECRET = inputX("Enter your Client Secret: ")
    anilistConfigJson = {
      "aniclient" : ANICLIENT,
      "anisecret" : ANISECRET,
      "redirectUrl" : "https://anilist.co/api/v2/oauth/pin"
    }
    with open(anilistConfig, "w+", encoding='utf-8') as F:
      F.write(json.dumps(anilistConfigJson, ensure_ascii=False, indent=4).encode('utf8').decode())
  try:
    with open(anilistConfig) as f:
      configData = json.load(f)
    ANICLIENT = configData['aniclient']
    ANISECRET = configData['anisecret']
    REDIRECT_URL = configData['redirectUrl']
    # logger("\nClient: " + ANICLIENT + "\nSecret: " + ANISECRET)
    useOAuth = True
  except:
    logger(f"There's no correct {anilistConfig} file!")
    useOAuth = False
    accessToken = ""
  
  if useOAuth:
    # Get OAuth and Access Token
    logger("Login Anilist on browser, and Authorize AniPy")
    url = f"https://anilist.co/api/v2/oauth/authorize?client_id={ANICLIENT}&redirect_uri={REDIRECT_URL}&response_type=code"
    webbrowser.open(url)

    code = inputX("Paste your token code here (Copied from Anilist webpage result): ")
    accessToken = fReq.request_accesstkn(ANICLIENT, ANISECRET, REDIRECT_URL, code)
    #logger("Access Token: [" + accessToken + "]")

  if accessToken:
    useOAuth = True
    logger("Has access token!")
  else:
    useOAuth = False
    logger("Cannot Authenticate! Will use Public Username.")
else:
  useOAuth = False


# Check whether authenticated, or use public Username
if not useOAuth:
  logger("'Public Username' Mode")
  accessToken = ""
  while (userID < 1):
    # Get Username
    username = inputX("Enter your Anilist Username: ")
    userID = fReq.anilist_getUserID(username)
else:
  logger("Getting User ID, from Authenticated user..")
  try:
    resultUserID = requests.post("https://graphql.anilist.co", headers={"Authorization": f"Bearer {accessToken}"}, json={"query": "{Viewer{id}}"}).json()
    userID = resultUserID["data"]["Viewer"]["id"]
    logger("User ID: " + str(userID))
  except:
    logger("User Id cannot be fetched!")

# Delete prev files
fMain.deleteFile(entryLog)

# Request anime list
outputAnime = getMediaEntries("ANIME", accessToken, userID, username, PROJECT_PATH, entryLog, useOAuth)

# Request manga list
outputManga = getMediaEntries("MANGA", accessToken, userID, username, PROJECT_PATH, entryLog, useOAuth)

# Trim List
tempTrim = inputX("Trim list (Create list of Entries not on MAL)? [y/n]: ")
if tempTrim.lower()[0] == "y":
  fTrim.trim_results(PROJECT_PATH, outputAnime, outputManga)

# Get Entries not on Tachi
tempTachi = inputX("Tachiyomi library json file (legacy backup): ")
if tempTachi:
  fNotOnTachi.getNotOnTachi(outputManga, tempTachi)

inputX("Press <Enter> to exit..")
