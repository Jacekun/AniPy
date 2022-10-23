# imports
import os
# Local Imports
import func.main as fMain
import func.anilist_request as fReq
from func.anilist_getMedia import getMediaEntries
import func.trim_list as fTrim
import func.getNotOnTachi as fNotOnTachi

# App Properties
appVersion = '1.20'
appMode = 'AniPy (Easy)'
mainsrc = "App"

def main():
  # Declare variables
  fMain.logString("Define Global Vars..", mainsrc)
  # Paths for Files
  PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) #os.path.dirname(sys.executable)
  fMain.logString("Current path: " + PROJECT_PATH, mainsrc)
  anilistConfig = os.path.join(PROJECT_PATH, "anilistConfig.json")
  entryLog = os.path.join(PROJECT_PATH, "output", "entries.log") # Log entries
  # Vars for Authentication
  ANICLIENT = ""
  ANISECRET = ""
  useOAuth = False
  # User vars
  userAnilist = None
  userMal = None
  userID = 0
  isSepNsfw = False # Separate nsfw entries on output
  # Output files dictionary
  outputAnime = []
  outputManga = []

  # Create 'output' directory
  if not os.path.exists('output'):
      os.makedirs('output')

  # Toggle when skipping Public mode, or Authenticated mode
  inputChoice = fMain.inputX("Use Authenticated mode? [y/n] (Default: 'Public List mode'): ", "n")

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

  # Ask for MAL username
  userMal = fMain.inputX("Enter your MAL Username: ", "")

  # Check whether authenticated, or use public Username
  if not useOAuth:
    fMain.logString("'Public Username' Mode", mainsrc)
    accessToken = ""
    while (userID < 1):
      # Get Anilist Username
      userAnilist = fMain.inputX("Enter your Anilist Username: ", "")
      userID = fReq.anilist_getUserID(userAnilist)
  else:
    fMain.logString("Getting User ID, from Authenticated user..", mainsrc)
    userID = fReq.anilist_getUserID_auth(accessToken)
    if userID is not None:
      fMain.logString("User ID: " + str(userID), mainsrc)
    else:
      fMain.logString("User Id cannot be fetched!", mainsrc)

  # Confirm if separating nsfw entries on generating output files
  inputChoice = fMain.inputX("Separate NSFW entries? [y/n] (Default: n): ", "n")

  if inputChoice.lower()[0] == "y":
    isSepNsfw = True

  # Delete prev files
  fMain.deleteFile(entryLog)

  # Initiate parameter values
  paramvals = {
      'root': PROJECT_PATH,
      'log': entryLog,
      'access_tkn': accessToken,
      'user_id': userID,
      'user_anilist': userAnilist,
      'user_mal': userMal,
      'use_auth': useOAuth,
      'sep_nsfw': isSepNsfw
  }

  # Request anime list
  outputAnime = getMediaEntries("ANIME", paramvals)

  # Request manga list
  outputManga = getMediaEntries("MANGA", paramvals)

  # Trim List
  tempTrim = fMain.inputX("Trim list (Create list of Entries not on MAL)? [y/n] (Default: n): ", "n")

  if tempTrim.lower()[0] == "y":
    fTrim.trim_results(PROJECT_PATH, outputAnime.get('main'), outputManga.get('main'), False)
    if isSepNsfw:
      fTrim.trim_results(PROJECT_PATH, outputAnime.get('nsfw'), outputManga.get('nsfw'), True)

  # Get Entries not on Tachi
  tempTachi = fMain.inputX("Tachiyomi backup file (json, proto, gz): ", None)
  if tempTachi:
    fNotOnTachi.getNotOnTachi(outputManga.get('main'), tempTachi, False)
    if isSepNsfw:
      fNotOnTachi.getNotOnTachi(outputManga.get('nsfw'), tempTachi, True)

  fMain.inputX("Press <Enter> to exit..", "")


if __name__ == "__main__":
  main()