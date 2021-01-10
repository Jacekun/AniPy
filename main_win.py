# imports
print("Importing packages..")
import os
import pygubu
import importlib
import sys
import pygubu.builder.tkstdwidgets
import pygubu.builder.ttkstdwidgets
from datetime import datetime

# Log string, and return it
def logger(text):
  print(f'[{datetime.now().strftime("%H:%M:%S")}][main_win]: {text}')
  return text

# Import Dynamic scripts
logger("Import scripts from same folder")
fMain = importlib.import_module("func.main")
fReq = importlib.import_module("func.anilist_request")
fGetAnime = importlib.import_module("func.anilist_getAnime")
fGetManga = importlib.import_module("func.anilist_getManga")
fTrim = importlib.import_module("func.trim_list")

# App Properties
appVersion = '1.2.0.9'
appBuild = 3

# Global Vars
logger("Define Global Vars..")
# Paths for Files
PROJECT_PATH = os.path.dirname(sys.executable)
logger("Current path: " + PROJECT_PATH)

PROJECT_UI = os.path.join(PROJECT_PATH, "files\\main_win.ui")
# Output file names
outputAnime = ""
outputManga = ""
entryLog = os.path.join(PROJECT_PATH, "output\\entries.log") # Log entries

# Objects
# List of IDs, to prevent duplicates
entryID = []

# Start App
class Main:
  logger("Define class Main()")
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

        # Delete prev files
        logger("Deleting previous 'entries.log'..")
        fMain.deleteFile(entryLog)

        # Request anime list
        labelStatus["text"] = logger("Requesting anime list..")
        fMain.write_append(entryLog, f'ANIME [{datetime.now().strftime("%Y-%m-%d")} {datetime.now().strftime("%H:%M:%S")}]\n')
        outputAnime = fGetAnime.getAnimeEntries(userID, username, PROJECT_PATH, entryLog)

        # Request manga list
        labelStatus["text"] = logger("Requesting manga list..")
        fMain.write_append(entryLog, f'MANGA [{datetime.now().strftime("%Y-%m-%d")} {datetime.now().strftime("%H:%M:%S")}]\n')
        outputManga = fGetManga.getMangaEntries(userID, username, PROJECT_PATH, entryLog)

        # Trim List
        labelStatus["text"] = logger("Trimming list..")
        fTrim.trim_results(PROJECT_PATH, outputAnime, outputManga)

        # Done
        labelStatus["text"] = logger("Done!")
       
    else:
      logger("Username is empty!")

    # Enable button
    buttonExport["state"] = "active"
    labelStatus["text"] = "Done!"

if __name__ == '__main__':
  logger("Run __main__ Main() class")
  app = Main()
  app.run()