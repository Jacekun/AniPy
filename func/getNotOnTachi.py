# Get entries in Anilist, not on your Tachiyomi library
# imports
import os
import json
import importlib
from datetime import datetime

# Other vars
logSrc = "getNotOnTachi"
tempAnilist = ""
tempTachi = ""
listTachiTracked = []
listSkippedStatus = [ "COMPLETED", "DROPPED" ]

# Functions
def logString(text, source="getNotOnTachi"):
  print(f'[{datetime.now().strftime("%H:%M:%S")}][{source}]: {text}')
  return text

def deleteFile(file):
    if os.path.exists(file):
        os.remove(file)

def sort_byval(json):
    try:
        return str(json['format'])
    except KeyError:
        return ""

def getNotOnTachi(inputManga, inputTachi):
    # Declare filepaths
    outputManga = inputManga[:-5] + "_NotInTachi.json"
    outputTachiBackup = inputManga[:-5] + "_TachiyomiBackup.json"
    TachiBackupJson = {
        "version": 2,
        "mangas": [],
        "categories": [
            [ "Anilist", 0 ]
        ]
    }

    # Delete previous file
    deleteFile(outputManga)

    # json Objects
    jsonOutputManga = []

    # Load JSON objects
    # Load Anilist MANGA
    if not (os.path.exists(inputManga)):
        logString(f"File: {inputManga} does not exists!", logSrc)
        jsonManga = None
    else:
        logString("Loading " + os.path.basename(inputManga) + " into memory..", logSrc)
        with open(inputManga, "r+", encoding='utf-8') as F:
            jsonManga = json.load(F)
            jsonManga.sort(key=sort_byval, reverse=True)
            logString("File loaded!", logSrc)
    
    # Load Tachiyomi Library
    if not (os.path.exists(inputTachi)):
        logString(f"File: {inputTachi} does not exists!", logSrc)
        tachiManga = None
    else:
        logString("Loading " + os.path.basename(inputTachi) + " into memory..")
        with open(inputTachi, "r+", encoding='utf-8') as F:
            tachiManga = json.load(F)
            logString("File loaded!")

    # Get entries from Tachiyomi, and turn into simple list
    if tachiManga is not None:
        logString("Checking Tachiyomi library..")
        for tachiEntry in tachiManga["mangas"]:
            try:
                tempTracker = tachiEntry["track"]
                if tempTracker is not None:
                    for tachiTrack in tempTracker:
                        tempTrackLink = str(tachiTrack["u"])
                        if "anilist" in tempTrackLink:
                            # logString("Id: [" + tempTrackLink[25:] + "]")
                            # listTachiTracked.append(tempTrackLink[25:])
                            listTachiTracked.append(str(tachiTrack["r"]))
            except:
                # logString("No tracking!")
                pass

    # Skip if no tachi library is provided
    if not listTachiTracked:
        logString("Tachiyomi library checking skipped!")
    # Else, continue
    else:
        # Get entries from Anilist Manga, and dispose entries already on Tachi tracked lib
        if jsonManga is not None:
            logString("Checking Anilist manga entries..")
            for entry in jsonManga:
                if str(entry["idAnilist"]) not in listTachiTracked:
                    jsonData = {}
                    jsonData["idAnilist"] = entry["idAnilist"]
                    jsonData["titleEnglish"] = entry["titleEnglish"]
                    jsonData["titleRomaji"] = entry["titleRomaji"]
                    if str(entry["synonyms"]) == "[]":
                        jsonData["synonyms"] = ""
                    else:
                        jsonData["synonyms"] = entry["synonyms"]
                    jsonData["status"] = entry["status"]
                    # Append to JSON object
                    if str(entry["status"]) not in listSkippedStatus:
                        if str(entry["format"]) != "NOVEL":
                            jsonOutputManga.append(jsonData) # add to json list of manga_NotInTachi
                            # Add to Tachiyomi backup json
                            titleEntry = ""
                            if jsonData["titleRomaji"] is not None:
                                titleEntry = jsonData["titleRomaji"]
                                if titleEntry.isspace():
                                    if jsonData["titleEnglish"] is not None:
                                        titleEntry = jsonData["titleEnglish"]
                            TachiBackupEntry = {
                                "manga": [
                                    titleEntry,
                                    titleEntry,
                                    0,
                                    0,
                                    0
                                ],
                                "categories": [
                                    "Anilist"
                                ]
                            }
                            TachiBackupJson["mangas"].append(TachiBackupEntry)
                    
            # Write 'outputManga': manga_NotInTachi
            logString("Writing to file " + os.path.basename(outputManga))
            with open(outputManga, "w+", encoding='utf-8') as F:
                F.write(json.dumps(jsonOutputManga, ensure_ascii=False, indent=4).encode('utf8').decode())
                logString("File generated: " + outputManga)
            # Write TachiBackupJson to file: __TachiyomiBackup.json
            logString("Writing to file " + os.path.basename(outputTachiBackup))
            with open(outputTachiBackup, "w+", encoding='utf-8') as F:
                F.write(json.dumps(TachiBackupJson, ensure_ascii=False, indent=4).encode('utf8').decode())
                logString("File generated: " + outputTachiBackup)