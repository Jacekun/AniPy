# Get entries in Anilist, not on your Tachiyomi library
# imports
import os
import json
from google import protobuf
# Local import
import func.main as fMain
from func import tachiBackup_pb2 as tachiBackupProto

fMain.logString("Imported func.getNotOnTachi", "")

# Functions
def logString(text):
  fMain.logString(text, "getNotOnTachi")

def sort_byval(json):
    try:
        return str(json['format'])
    except KeyError:
        return ""

# Open json tachiyomi backup file, and load all Anilist-tracked entries
def parseLegacyBackup(inputMangaPath: str) -> list:
    listReturn = []
    loadTachi = None
    logString("Loading legacy backup '" + os.path.basename(inputMangaPath) + "' into memory..")
    with open(inputMangaPath, "r+", encoding='utf-8') as F:
        loadTachi = json.load(F)
        logString("Tachi library json file loaded!")
    
    # Get entries from Tachiyomi json (legacy backup), and turn into simple list
    if loadTachi is not None:
        logString("Checking Tachiyomi library..")
        for tachiEntry in loadTachi["mangas"]:
            try:
                tempTracker = tachiEntry["track"]
                if tempTracker is not None:
                    for tachiTrack in tempTracker:
                        tempTrackLink = str(tachiTrack["u"])
                        if "anilist" in tempTrackLink:
                            # logString("Id: [" + tempTrackLink[25:] + "]")
                            # listReturn.append(tempTrackLink[25:])
                            listReturn.append(str(tachiTrack["r"]))
            except:
                # logString("No tracking!")
                pass
    return listReturn

# Open proto tachiyomi backup file, and load all Anilist-tracked entries
def parseProtoBackup(inputMangaPath: str) -> list:
    listReturn = []
    #logString("Loading backup: " + inputMangaPath)
    logString("Loading backup '" + os.path.basename(inputMangaPath) + "' into memory..")
    _backupManga = None
    try:
        with open(inputMangaPath, "rb") as f:
            logString("Initiating backup..")
            _backupManga = tachiBackupProto.Backup()
            logString("Parsing backup..")
            _backupManga.ParseFromString(f.read())
            
        if _backupManga is not None:
            logString("Backup file has contents!")
            _backupMangaList = _backupManga.backupManga
            logString("Accessed Backup root!")
            if _backupMangaList is not None:
                logString("Backup file has manga list!")
                for _entry in _backupMangaList:
                    if _entry is not None:
                        #logString("Parsing: " + _entry.title)
                        _trackers = _entry.tracking
                        if _trackers:
                            for _track in _trackers:
                                if _track is not None:
                                    if str(_track.syncId) == "2":
                                        listReturn.append(str(_track.mediaId))
                                        break
    except Exception as e:
        logString("Exception on reading backup!")
        print(e)
    return listReturn

# Function called on main script
def getNotOnTachi(inputManga: str, inputTachi: str, isNsfw: bool):
    # Vars
    logSrc = "getNotOnTachi"
    listTachiTracked = []
    listSkippedStatus = [ "COMPLETED", "DROPPED" ]

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
    fMain.deleteFile(outputManga)

    # json Objects
    jsonOutputManga = []

    # Load Tachiyomi Library
    if not (os.path.exists(inputTachi)):
        logString("Tachiyomi library does not exists!")
    else:
        if inputTachi[-4:] == "json":
            listTachiTracked = parseLegacyBackup(inputTachi)
        elif inputTachi[-5:] == "proto":
            listTachiTracked = parseProtoBackup(inputTachi)
        elif inputTachi[-2:] == "gz":
            extracted = fMain.extractGz(inputTachi)
            listTachiTracked = parseProtoBackup(extracted)
        else:
            logString("Unrecognized Tachiyomi backup file! Make sure you use Tachiyomi's legacy backup (File ends with .json)")

    # Skip if tachi backup has no tracked entries
    if not listTachiTracked:
        logString("No tracked Manga on Tachiyomi backup file!")
    # Else, continue
    else:
        # Load Anilist MANGA
        if not (os.path.exists(inputManga)):
            logString("Manga data file does not exists!")
            jsonManga = None
        else:
            logString("Loading " + os.path.basename(inputManga) + " into memory..")
            with open(inputManga, "r+", encoding='utf-8') as F:
                jsonManga = json.load(F)
                jsonManga.sort(key=sort_byval, reverse=True)
                logString("Manga JSON File loaded!")
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
                            if jsonData["titleEnglish"] is not None:
                                titleEntry = jsonData["titleEnglish"]
                                if not titleEntry:
                                    if jsonData["titleRomaji"] is not None:
                                        titleEntry = jsonData["titleRomaji"]
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
            fMain.createJsonFile(outputManga, jsonOutputManga, logSrc)
            # Write TachiBackupJson to file: __TachiyomiBackup.json
            fMain.createJsonFile(outputTachiBackup, TachiBackupJson, logSrc)