# imports
import os
import sys
import importlib
from datetime import datetime

# Logger
def logger(text):
    print("[" + '{0:%H:%M:%S}'.format(datetime.now()) + "]: " + text)
    
logger("Define Global Vars..")
# Global Vars

# Paths for Files
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__)) #os.path.dirname(sys.executable)
PROJECT_UI = os.path.join(PROJECT_PATH, "files\\main_win.ui")
logger("Current path: " + PROJECT_PATH)

# Import libs from 'func'
logger("Import scripts from same folder")
fMain = importlib.import_module("func.main")
fReq = importlib.import_module("func.anilist_request")
fGetAnime = importlib.import_module("func.anilist_getAnime")
fGetManga = importlib.import_module("func.anilist_getManga")
fTrim = importlib.import_module("func.trim_list")

# App Properties
appVersion = '1.2.0.5'
appBuild = 2

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

# Start of 'Main' class
class MainApp:
  logger("Starting console app..")
  # Exit if username is null
  if (username is not None):

    while (userID < 1):
      # Get Username
      username = input("Enter your Anilist Username: ")
      userID = fReq.anilist_getUserID(username)

    # Check if User ID is valid
    if (userID > 0):
      
      # Delete prev files
      fMain.deleteFile(entryLog)

      # Request anime list
      fMain.write_append(entryLog, f'ANIME [{datetime.now().strftime("%Y-%m-%d")} {datetime.now().strftime("%H:%M:%S")}]\n')
      outputAnime = fGetAnime.getAnimeEntries(userID, username, PROJECT_PATH, entryLog)

      # Request manga list
      fMain.write_append(entryLog, f'MANGA [{datetime.now().strftime("%Y-%m-%d")} {datetime.now().strftime("%H:%M:%S")}]\n')
      outputManga = fGetManga.getMangaEntries(userID, username, PROJECT_PATH, entryLog)

      # Trim List
      fTrim.trim_results(PROJECT_PATH, outputAnime, outputManga)

  else:
    logger("Username is empty!")