# imports
print("Import packages..")
import os
import pygubu
import importlib
import sys
import pygubu.builder.tkstdwidgets
import pygubu.builder.ttkstdwidgets
from datetime import datetime

# Log string, and return it
def logger(text):
  print("[" + '{0:%H:%M:%S}'.format(datetime.now()) + "]: " + text)

# Import Dynamic scripts
logger("Import scripts from same folder")
fMain = importlib.import_module("func.main")
fReq = importlib.import_module("func.anilist_request")
fGetAnime = importlib.import_module("func.anilist_getAnime")
fGetManga = importlib.import_module("func.anilist_getManga")
fTrim = importlib.import_module("func.trim_list")

# App Properties
appVersion = '1.2.0.4'
appBuild = 3

# Global Vars
logger("Define Global Vars..")
# Paths for Files
PROJECT_PATH = os.path.dirname(sys.executable) #os.path.dirname(__file__)
logger("Current path: " + PROJECT_PATH)

PROJECT_UI = os.path.join(PROJECT_PATH, "files\\main_win.ui")
entryLog = os.path.join(PROJECT_PATH, "entries.log") # Log entries
# Output file names
outputAnime = os.path.join(PROJECT_PATH, "output\\anime.json")
xmlAnime = os.path.join(PROJECT_PATH, "output\\anime.xml")
outputManga = os.path.join(PROJECT_PATH, "output\\manga.json")
xmlManga = os.path.join(PROJECT_PATH, "output\\manga.xml")
entryLog = os.path.join(PROJECT_PATH, "output\\entries.log")
# Trim List Output
outputAnimeTrim = os.path.join(PROJECT_PATH, "output\\anime_NotInMal.json")
outputMangaTrim = os.path.join(PROJECT_PATH, "output\\manga_NotInMal.json")
outputStats = os.path.join(PROJECT_PATH, "output\\animemanga_stats.txt")

# Objects
# List of IDs, to prevent duplicates
entryID = []

logger("Start App from Class: 'Main'.")
# Start App
class Main:
  # GUI
  def __init__(self, master=None):
    # build ui
    self.builder = builder = pygubu.Builder()
    builder.add_resource_path(PROJECT_PATH)
    builder.add_from_file(PROJECT_UI)
    self.mainwindow = builder.get_object('gTopLevel')
    builder.connect_callbacks(self)

  def run(self):
    self.mainwindow.mainloop()

  # events
  def buttonExport_callback(self):
    # Get object IDs
    buttonExport = self.builder.get_object('gButtonExport')
    labelStatus = self.builder.get_object('gLabelStatus')

    # Disable button
    labelStatus.config(text = "Starting export..")
    buttonExport["state"] = "disabled"

    # Get User ID, from Username
    labelStatus["text"] = "Getting user ID.."
    username = fMain.validateStr(self.builder.tkvariables['inputUser'].get())
    # Exit if username is null
    if (username is not None):
      # Get User ID, by POST-ing a request to Anilist
      userID = fReq.anilist_getUserID(username)
      if (userID > 0):
        labelStatus["text"] = "User ID received!"
        logger("Successfully received the user ID!")

        # Request anime list
        labelStatus["text"] = fMain.logString("Requesting anime list..")
        fGetAnime.getAnimeEntries(userID, username, outputAnime, xmlAnime, entryLog)

        # Request manga list
        labelStatus["text"] = fMain.logString("Requesting manga list..")
        fGetManga.getMangaEntries(userID, username, outputManga, xmlManga, entryLog)

        # Trim List
        labelStatus["text"] = fMain.logString("Trimming list..")
        fTrim.trim_results(outputAnime, outputManga, outputAnimeTrim, outputMangaTrim, outputStats)

        # Done
        labelStatus["text"] = fMain.logString("Done!")
       
    else:
      logger("Username is empty!")

    # Enable button
    buttonExport["state"] = "active"
    labelStatus["text"] = "Done!"

if __name__ == '__main__':
  app = Main()
  app.run()