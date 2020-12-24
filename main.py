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
PROJECT_PATH = os.path.dirname(sys.executable) #os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "files\\main_win.ui")
logger("Current path: " + PROJECT_PATH)

# Import libs from 'func'
logger("Import scripts from same folder")
fMain = importlib.import_module("func.func")
fReq = importlib.import_module("func.anilist_request")

# App Properties
appVersion = '1.1.0.0'
appBuild = 2

# Get Username
username = input("Enter your Anilist Username: ")
userID = 0
# Output file names
outputAnime = "anime.json"
xmlAnime = "anime.xml"
outputManga = "manga.json"
xmlManga = "manga.xml"
entryLog = "entries.log" # Log entries
# json objects
jsonAnime = None
# List of IDs, to prevent duplicates
entryID = []

# Start of 'Main' class
class MainApp:
  logger("Starting console app..")
  # Exit if username is null
  if (username is not None):
    userID = fReq.anilist_getUserID(username)
    # Check if User ID is valid
    if (userID > 0):
      # Check if not existing
      if not (os.path.exists(outputAnime)):
        # Get JSON object
        jsonAnime = fReq.anilist_userlist(userID, "ANIME")

        # Check if not null
        if jsonAnime is not None:
          listAnime = jsonAnime["data"]["MediaListCollection"]["lists"]

          # Create vars
          # Count Manga entries
          cTotal = 0
          cWatch = 0
          cComplete = 0
          cHold = 0
          cDrop = 0
          cPtw = 0

          # Start generating JSON and XML..
          # Write to json file
          fMain.write_append(outputAnime, '[\n')

          # Log duplicate entries
          fMain.write_append(entryLog, "ANIME Entries Log\n")
          entryID.clear() # Clear list

          # Iterate over the MediaCollection List
          for anime in listAnime:
            # Get entries
            animeInfo = anime["entries"]
            # Iterate over the anime information, inside the entries
            for entry in animeInfo:
              # Get Anilist ID
              anilistID = entry["media"]["id"]
              # Check if already exists
              if anilistID in entryID:
                fMain.write_append(entryLog, "Skipped: " + str(anilistID) + ", Duplicate Anime entry.\n")
                continue
              else:
                entryID.append(anilistID)

              # Write to json file
              jsontoAdd = fMain.entry_json(entry, 'anime')
              fMain.write_append(outputAnime, jsontoAdd)

              # Write to MAL Xml File
              malID = fMain.validateInt(entry["media"]["idMal"])
              if malID != '0':
                # Get XML strings
                xmltoWrite = fMain.entry_animexml(malID, entry)
                # Write to xml file
                fMain.write_append(xmlAnime, xmltoWrite)
              
                # Add count
                malstatus = fMain.validateStr(entry["status"])
                if (malstatus == "COMPLETED"):
                  cComplete = cComplete + 1
                elif (malstatus == "PAUSED"):
                  cHold = cHold + 1
                elif (malstatus == "CURRENT"):
                  cWatch = cWatch + 1
                elif (malstatus == "DROPPED"):
                  cDrop = cDrop + 1
                elif (malstatus == "PLANNING"):
                  cPtw = cPtw + 1

          # Delete last comma ',', in json file
          logger("Remove last comma from Anime JSON file..")
          fMain.write_remove(outputAnime, 3)

          # Write ']' at the end, to json file
          logger("Write last ']' to Anime JSON file..")
          fMain.write_append(outputAnime, '\n]')
          logger("Done with Anime JSON file..")
          
          # Write to MAL xml file
          logger("Finalizing Anime XML file..")
          fMain.write_append(xmlAnime, '</myanimelist>')

          # Total counts
          cTotal = cWatch + cComplete + cHold + cDrop + cPtw
          logger("Prepend 'myinfo' to Anime XML file..")
          malprepend = '<?xml version="1.0" encoding="UTF-8" ?>\n<myanimelist>\n'
          malprepend += '\t<myinfo>\n'
          malprepend += '\t\t' + fMain.toMalval('', 'user_id') + '\n'
          malprepend += '\t\t' + fMain.toMalval(username, 'user_name') + '\n'
          malprepend += '\t\t' + fMain.toMalval('1', 'user_export_type') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cTotal), 'user_total_anime') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cWatch), 'user_total_watching') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cComplete), 'user_total_completed') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cHold), 'user_total_onhold') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cDrop), 'user_total_dropped') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cPtw), 'user_total_plantowatch') + '\n'
          malprepend += '\t</myinfo>\n'
          fMain.line_prepender(xmlAnime, malprepend)
          logger("Done with Anime XML file..")

          # Done anime
          logger("Done! File generated: " + outputAnime)
          logger("Done! File generated: " + xmlAnime)

      # Already existing!
      else:
        logger(outputAnime + " file already exist!")
      
      # Request manga list
      # Check if not existing
      if not (os.path.exists(outputManga)):
        # Get JSON object
        jsonManga = fReq.anilist_userlist(userID, "MANGA")

        # Check if not null
        if jsonManga is not None:
          listManga = jsonManga["data"]["MediaListCollection"]["lists"]

          # Create vars
          # Count Manga entries
          cTotal = 0
          cRead = 0
          cComplete = 0
          cHold = 0
          cDrop = 0
          cPtr = 0

          # Start generating JSON and XML..
          # Write to json file
          fMain.write_append(outputManga, '[\n')

          # Log duplicate entries
          fMain.write_append(entryLog, "MANGA Entries Log\n")
          entryID.clear() # Clear list

          # Iterate over the MediaCollection List
          for manga in listManga:
            # Get Manga Entries
            mangaInfo = manga["entries"]
            # Iterate over the manga information, inside the entries
            for entry in mangaInfo:
              # Get Anilist ID
              anilistID = entry["media"]["id"]
              # Check if already exists
              if anilistID in entryID:
                fMain.write_append(entryLog, "Skipped: " + str(anilistID) + ", Duplicate Manga entry.\n")
                continue
              else:
                entryID.append(anilistID)

              # Write to json file
              jsontoAdd = fMain.entry_json(entry, 'manga')
              fMain.write_append(outputManga, jsontoAdd)

              # Write to MAL Xml File
              malID = fMain.validateInt(entry["media"]["idMal"])
              if malID != '0':
                # Get XML strings
                xmltoWrite = fMain.entry_mangaxml(malID, entry)
                # Write to xml file
                fMain.write_append(xmlManga, xmltoWrite)

                # Add count
                malstatus = fMain.validateStr(entry["status"])
                if (malstatus == "COMPLETED"):
                  cComplete = cComplete + 1
                elif (malstatus == "PAUSED"):
                  cHold = cHold + 1
                elif (malstatus == "CURRENT"):
                  cRead = cRead + 1
                elif (malstatus == "DROPPED"):
                  cDrop = cDrop + 1
                elif (malstatus == "PLANNING"):
                  cPtr = cPtr + 1

        # Delete last comma ',', in json file
        logger("Remove last comma from manga JSON file..")
        fMain.write_remove(outputManga, 3)

        # Write ']' at the end, to json file
        logger("Write last ']' to manga JSON file..")
        fMain.write_append(outputManga, '\n]')
        logger("Done with Manga JSON file..")
        
        # Write to MAL xml file
        logger("Finalizing Manga XML file..")
        fMain.write_append(xmlManga, '</myanimelist>')

        # Total counts
        cTotal = cRead + cComplete + cHold + cDrop + cPtr
        logger("Prepend 'myinfo' to Manga XML file..")
        malprepend = '<?xml version="1.0" encoding="UTF-8" ?>\n<myanimelist>\n'
        malprepend += '\t<myinfo>\n'
        malprepend += '\t\t' + fMain.toMalval('', 'user_id') + '\n'
        malprepend += '\t\t' + fMain.toMalval(username, 'user_name') + '\n'
        malprepend += '\t\t' + fMain.toMalval('2', 'user_export_type') + '\n'
        malprepend += '\t\t' + fMain.toMalval(str(cTotal), 'user_total_manga') + '\n'
        malprepend += '\t\t' + fMain.toMalval(str(cRead), 'user_total_reading') + '\n'
        malprepend += '\t\t' + fMain.toMalval(str(cComplete), 'user_total_completed') + '\n'
        malprepend += '\t\t' + fMain.toMalval(str(cHold), 'user_total_onhold') + '\n'
        malprepend += '\t\t' + fMain.toMalval(str(cDrop), 'user_total_dropped') + '\n'
        malprepend += '\t\t' + fMain.toMalval(str(cPtr), 'user_total_plantoread') + '\n'
        malprepend += '\t</myinfo>\n'
        fMain.line_prepender(xmlManga, malprepend)
        logger("Done with Manga XML file..")

        # Done manga
        logger("Done! File generated: " + outputManga)
        logger("Done! File generated: " + xmlManga)

      else:
        logger(outputManga + " file already exist!")

  else:
    logger("Username is empty!")