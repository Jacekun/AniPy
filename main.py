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
appVersion = '1.2.0.4'
appBuild = 2

# User vars
username = ""
userID = 0
# Output file names
outputAnime = os.path.join(PROJECT_PATH, "output\\anime.json")
xmlAnime = os.path.join(PROJECT_PATH, "output\\anime.xml")
outputManga = os.path.join(PROJECT_PATH, "output\\manga.json")
xmlManga = os.path.join(PROJECT_PATH, "output\\manga.xml")
entryLog = os.path.join(PROJECT_PATH, "output\\entries.log") # Log entries
# Trim List Output
outputAnimeTrim = os.path.join(PROJECT_PATH, "output\\anime_NotInMal.json")
outputMangaTrim = os.path.join(PROJECT_PATH, "output\\manga_NotInMal.json")
outputStats = os.path.join(PROJECT_PATH, "output\\animemanga_stats.txt")
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
      
      # Request anime list
      fGetAnime.getAnimeEntries(userID, username, outputAnime, xmlAnime, entryLog)

      # Request manga list
      fGetManga.getMangaEntries(userID, username, outputManga, xmlManga, entryLog)

      # Trim List
      fTrim.trim_results(outputAnime, outputManga, outputAnimeTrim, outputMangaTrim, outputStats)

  else:
    logger("Username is empty!")