# imports
import os
import json
import requests
from datetime import datetime
# Local Imports
import func.main as fMain
import func.anilist_request as fReq
from func.anilist_getMedia import getMediaEntries
import func.trim_list as fTrim
import func.getNotOnTachi as fNotOnTachi

# App Properties
appVersion = '1.13'
appMode = 'AniPy (Easy)'
mainsrc = "App"

def main():
  # Declare variables
  fMain.logString("Define Global Vars..", mainsrc)
  # Paths for Files
  PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) #os.path.dirname(sys.executable)
  fMain.logString("Current path: " + PROJECT_PATH, mainsrc)
  anilistConfig = os.path.join(PROJECT_PATH, "anilistConfig.json")
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

  # Toggle when skipping Public mode, or Authenticated mode
  inputChoice = fMain.inputX("Type 'yes' or 'y' to Use Authenticated mode (Default: 'Public mode'): ")
  if not inputChoice:
    inputChoice = "n"

  if inputChoice.lower()[0] == "y":
    # Import config for Anilist OAuth
    fMain.logString("Importing Anilist config", mainsrc)
    
    useOAuth, ANICLIENT, ANISECRET, REDIRECT_URL = fReq.setup_config(anilistConfig)

    if not useOAuth:
      accessToken = ""
    
    if useOAuth:
      code = fReq.request_pubcode(ANICLIENT, REDIRECT_URL)
      accessToken = fReq.request_accesstkn(ANICLIENT, ANISECRET, REDIRECT_URL, code)

    if accessToken:
      useOAuth = True
      fMain.logString("Has access token!", mainsrc)
    else:
      useOAuth = False
      fMain.logString("Cannot Authenticate! Will use Public Username.", mainsrc)
  else:
    useOAuth = False


  # Check whether authenticated, or use public Username
  if not useOAuth:
    fMain.logString("'Public Username' Mode", mainsrc)
    accessToken = ""
    while (userID < 1):
      # Get Anilist Username
      anilistUser = fMain.inputX("Enter your Anilist Username: ")
      userID = fReq.anilist_getUserID(anilistUser)
  else:
    fMain.logString("Getting User ID, from Authenticated user..", mainsrc)
    userID = fReq.anilist_getUserID_auth(accessToken)
    if userID is not None:
      fMain.logString("User ID: " + str(userID), mainsrc)
    else:
      fMain.logString("User Id cannot be fetched!", mainsrc)

  # Delete prev files
  fMain.deleteFile(entryLog)

  # Request anime list
  outputAnime = getMediaEntries("ANIME", accessToken, userID, username, PROJECT_PATH, entryLog, useOAuth)

  # Request manga list
  outputManga = getMediaEntries("MANGA", accessToken, userID, username, PROJECT_PATH, entryLog, useOAuth)

  # Trim List
  tempTrim = fMain.inputX("Trim list (Create list of Entries not on MAL)? [y/n] (Default: n): ")
  if not tempTrim:
    tempTrim = "n"
  if tempTrim.lower()[0] == "y":
    fTrim.trim_results(PROJECT_PATH, outputAnime.get('main'), outputManga.get('main'), False)
    fTrim.trim_results(PROJECT_PATH, outputAnime.get('nsfw'), outputManga.get('nsfw'), True)

  # Get Entries not on Tachi
  tempTachi = fMain.inputX("Tachiyomi library json file (legacy backup): ")
  if tempTachi:
    fNotOnTachi.getNotOnTachi(outputManga.get('main'), tempTachi, False)
    fNotOnTachi.getNotOnTachi(outputManga.get('nsfw'), tempTachi, True)

  fMain.inputX("Press <Enter> to exit..")


if __name__ == "__main__":
  main()