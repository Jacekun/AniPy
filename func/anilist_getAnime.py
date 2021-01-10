# Imports
import os
import importlib
from datetime import datetime

# Logger
def logger(text):
    print("[" + '{0:%H:%M:%S}'.format(datetime.now()) + "]: " + text)

# Import libs from 'func'
logger("Importing external modules..")
fMain = importlib.import_module("func.main")
fReq = importlib.import_module("func.anilist_request")
logger("Imported Modules!")

# List of IDs, to prevent duplicates
entryID = []

# Main Function
def getAnimeEntries(userID, username, filepath, entryLog):

    # Declare filepaths
    outputAnime = os.path.join(filepath, "output\\anime_" + datetime.now().strftime("%Y-%m-%d") + ".json")
    xmlAnime = os.path.join(filepath, "output\\anime_" + datetime.now().strftime("%Y-%m-%d") + ".xml")

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
                    # Get Anilist Status
                    AnilistStatus = fMain.validateStr(entry["status"])

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
                        if (AnilistStatus == "COMPLETED"):
                            cComplete = cComplete + 1
                        elif (AnilistStatus == "PAUSED"):
                            cHold = cHold + 1
                        elif (AnilistStatus == "CURRENT"):
                            cWatch = cWatch + 1
                        elif (AnilistStatus == "DROPPED"):
                            cDrop = cDrop + 1
                        elif (AnilistStatus == "PLANNING"):
                            cPtw = cPtw + 1
                        elif (AnilistStatus == "REPEATING"):
                            cWatch = cWatch + 1

            # Delete last comma ',', in json file
            fMain.logString("Remove last comma from Anime JSON file..")
            fMain.write_remove(outputAnime, 3)

            # Write ']' at the end, to json file
            fMain.logString("Write last ']' to Anime JSON file..")
            fMain.write_append(outputAnime, '\n]')
            fMain.logString("Done with Anime JSON file..")
            
            # Write to MAL xml file
            fMain.logString("Finalizing Anime XML file..")
            fMain.write_append(xmlAnime, '</myanimelist>')

            # Total counts
            cTotal = cWatch + cComplete + cHold + cDrop + cPtw
            fMain.logString("Prepend 'myinfo' to Anime XML file..")
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
            fMain.logString("Done with Anime XML file..")

            # Done anime
            fMain.logString("Done! File generated: " + outputAnime)
            fMain.logString("Done! File generated: " + xmlAnime)

    # Already existing!
    else:
        fMain.logString(outputAnime + " file already exist!")
    
    return outputAnime