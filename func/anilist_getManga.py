# Imports
import os
import importlib
from datetime import datetime

# Logger
def logger(text):
    print(f'[anilist_getManga][{datetime.now().strftime("%H:%M:%S")}]: {text}')

# Import libs from 'func'
logger("Importing external modules..")
fMain = importlib.import_module("func.main")
fReq = importlib.import_module("func.anilist_request")
logger("Imported Modules!")

# List of IDs, to prevent duplicates
entryID = []

# Main Function
def getMangaEntries(userID, username, filepath, entryLog):

    # Declare filepaths
    outputManga = os.path.join(filepath, "output\\manga_" + datetime.now().strftime("%Y-%m-%d") + ".json")
    xmlManga = os.path.join(filepath, "output\\manga_" + datetime.now().strftime("%Y-%m-%d") + ".xml")

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
              # Get Anilist Status
              AnilistStatus = fMain.validateStr(entry["status"])

              # Check if already exists
              if anilistID in entryID:
                fMain.write_append(entryLog, f'[{datetime.now().strftime("%Y-%m-%d")}] Skipped: {str(anilistID)}, Duplicate manga entry.\n')
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
                xmltoWrite = fMain.entry_mangaxml(malID, entry, str(AnilistStatus))
                # Write to xml file
                fMain.write_append(xmlManga, xmltoWrite)

                # Add count
                if (AnilistStatus == "COMPLETED"):
                  cComplete = cComplete + 1
                elif (AnilistStatus == "PAUSED"):
                  cHold = cHold + 1
                elif (AnilistStatus == "CURRENT"):
                  cRead = cRead + 1
                elif (AnilistStatus == "DROPPED"):
                  cDrop = cDrop + 1
                elif (AnilistStatus == "PLANNING"):
                  cPtr = cPtr + 1
                elif (AnilistStatus == "REPEATING"):
                  cRead = cRead + 1

        # Delete last comma ',', in json file
        fMain.logString("Remove last comma from manga JSON file..")
        fMain.write_remove(outputManga, 3)

        # Write ']' at the end, to json file
        fMain.logString("Write last ']' to manga JSON file..")
        fMain.write_append(outputManga, '\n]')
        fMain.logString("Done with Manga JSON file..")
        
        # Write to MAL xml file
        fMain.logString("Finalizing Manga XML file..")
        fMain.write_append(xmlManga, '</myanimelist>')

        # Total counts
        cTotal = cRead + cComplete + cHold + cDrop + cPtr
        fMain.logString("Prepend 'myinfo' to Manga XML file..")
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
        fMain.logString("Done with Manga XML file..")

        # Done manga
        fMain.logString("Done! File generated: " + outputManga)
        fMain.logString("Done! File generated: " + xmlManga)

    else:
        fMain.logString("Manga file already exist!: " + outputManga)

    return outputManga