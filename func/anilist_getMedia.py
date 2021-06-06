# Imports
import os
from datetime import datetime
# Local Imports
import func.main as fMain
import func.anilist_request as fReq

fMain.logString("Imported func.anilist_getMedia", "")

# Main Function
def getMediaEntries(mediaType, accessToken, userID, username, filepath, entryLog, useOAuth):
    # Vars and Objects
    entryID = [] # List of IDs, to prevent duplicates
    jsonToDump = [] # List of Json dict object of results
    source = "anilist_get" + mediaType
    fMain.logString("All vars are initiated", source)

    # Declare filepaths
    if mediaType == "ANIME":
        outputMedia = os.path.join(filepath, "output", "anime_" + datetime.now().strftime("%Y-%m-%d") + ".json")
        xmlMedia = os.path.join(filepath, "output", "anime_" + datetime.now().strftime("%Y-%m-%d") + ".xml")
    else:
        outputMedia = os.path.join(filepath, "output", "manga_" + datetime.now().strftime("%Y-%m-%d") + ".json")
        xmlMedia = os.path.join(filepath, "output", "manga_" + datetime.now().strftime("%Y-%m-%d") + ".xml")

    # Check if not existing
    if not (os.path.exists(outputMedia)):
        # Get JSON object
        if useOAuth:
            jsonMedia = fReq.anilist_userlist(accessToken, userID, mediaType)
        else:
            jsonMedia = fReq.anilist_userlist_public(userID, mediaType)

        # Check if not null
        if jsonMedia is not None:
            listMedia = jsonMedia["data"]["MediaListCollection"]["lists"]

            # Create vars
            # Count Manga entries
            cTotal = 0
            cWatch = 0
            cComplete = 0
            cHold = 0
            cDrop = 0
            cPtw = 0

            # Start generating JSON and XML..
            fMain.logString("Generating JSON and XML..", source)

            # Log duplicate entries
            fMain.write_append(entryLog, f'{mediaType} Entries [{datetime.now().strftime("%Y-%m-%d")} {datetime.now().strftime("%H:%M:%S")}]\n')
            entryID.clear() # Clear list

            # Iterate over the MediaCollection List
            for anime in listMedia:
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
                        fMain.write_append(entryLog, f'[{datetime.now().strftime("%Y-%m-%d")}] Skipped: {str(anilistID)}, Duplicate {mediaType} entry.\n')
                        continue
                    else:
                        entryID.append(anilistID)

                    # Write to json file
                    jsonToDump.append(fMain.entry_json(entry, mediaType))

                    # Write to MAL Xml File
                    malID = fMain.validateInt(entry["media"]["idMal"])
                    if malID != '0':
                        # Get XML strings
                        xmltoWrite = fMain.entry_xmlstr(mediaType, malID, entry, str(AnilistStatus))
                        # Write to xml file
                        fMain.write_append(xmlMedia, xmltoWrite)
                        
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

            # Dump JSON to file..
            if (fMain.dumpToJson(jsonToDump, outputMedia)):
                fMain.logString("Succesfully created json file!", source)
            else:
                fMain.logString("Error with creating json file!", source)
            fMain.logString(f"Done with {mediaType} JSON file..", source)
            
            # Write to MAL xml file
            fMain.logString(f"Finalizing {mediaType} XML file..", source)
            cTotal = cWatch + cComplete + cHold + cDrop + cPtw
            malprepend = ""

            if mediaType == "ANIME":
                fMain.write_append(xmlMedia, '</myanimelist>')
                # Total counts
                fMain.logString(f"Prepend 'myinfo' to {mediaType} XML file..", source)
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
            else:
                fMain.write_append(xmlMedia, '</mymangalist>')
                # Total counts
                fMain.logString(f"Prepend 'myinfo' to {mediaType} XML file..", source)
                malprepend = '<?xml version="1.0" encoding="UTF-8" ?>\n<mymangalist>\n'
                malprepend += '\t<myinfo>\n'
                malprepend += '\t\t' + fMain.toMalval('', 'user_id') + '\n'
                malprepend += '\t\t' + fMain.toMalval(username, 'user_name') + '\n'
                malprepend += '\t\t' + fMain.toMalval('2', 'user_export_type') + '\n'
                malprepend += '\t\t' + fMain.toMalval(str(cTotal), 'user_total_manga') + '\n'
                malprepend += '\t\t' + fMain.toMalval(str(cWatch), 'user_total_reading') + '\n'
                malprepend += '\t\t' + fMain.toMalval(str(cComplete), 'user_total_completed') + '\n'
                malprepend += '\t\t' + fMain.toMalval(str(cHold), 'user_total_onhold') + '\n'
                malprepend += '\t\t' + fMain.toMalval(str(cDrop), 'user_total_dropped') + '\n'
                malprepend += '\t\t' + fMain.toMalval(str(cPtw), 'user_total_plantoread') + '\n'
                malprepend += '\t</myinfo>\n'
                
            fMain.line_prepender(xmlMedia, malprepend)
            fMain.logString(f"Done with {mediaType} XML file..", source)

            # Done anime/manga
            fMain.logString("Done! File generated: " + outputMedia, source)
            fMain.logString("Done! File generated: " + xmlMedia, source)

    # Already existing!
    else:
        fMain.logString(f"{mediaType} file already exist!: " + outputMedia, source)
    
    return outputMedia
