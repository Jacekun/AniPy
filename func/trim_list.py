# Remove Entries that have MAL ID
# And additional code to get stats
# imports
import os
import json
# Local imports
import func.main as fMain

# Other vars
logSrc = "trim_list"
fMain.logString("Imported func.trim_list", "")

# Functions
def sort_byval(json):
    try:
        return str(json['format'])
    except KeyError:
        return ""

def trim_results(filepath, inputAnime, inputManga):
    # Declare filepaths
    outputStats = os.path.join(filepath, "output", "animemanga_stats.txt")
    outputAnime = inputAnime[:-5] + "_NotInMAL.json"
    outputManga = inputManga[:-5] + "_NotInMAL.json"
    # STATS variables
    statScoreTotal = 0
    statScoreCount = 0
    statInMAL = 0
    # Count entries
    cTotal = 0
    cCurrent = 0
    cComplete = 0
    cHold = 0
    cDrop = 0
    cPlan = 0

    # Delete prev files
    fMain.deleteFile(outputStats)

    # Load JSON objects
    # Check if anime file Exists!
    if not (os.path.exists(inputAnime)):
        fMain.logString("Anime json file does not exists!", logSrc)
        jsonAnime = None
    else:
        fMain.logString("Loading " + os.path.basename(inputAnime) + " into memory..", logSrc)
        with open(inputAnime, "r+", encoding='utf-8') as F:
            jsonAnime = json.load(F)
            jsonAnime.sort(key=sort_byval, reverse=True)
            fMain.logString("Anime json file loaded!", logSrc)
    # Check if manga file Exists!
    if not (os.path.exists(inputManga)):
        fMain.logString("Manga json file does not exists!", logSrc)
        jsonManga = None
    else:
        fMain.logString("Loading " + os.path.basename(inputManga) + " into memory..", logSrc)
        with open(inputManga, "r+", encoding='utf-8') as F:
            jsonManga = json.load(F)
            jsonManga.sort(key=sort_byval, reverse=True)
            fMain.logString("Manga json file loaded!", logSrc)

    # json Objects
    jsonOutputAnime = []
    jsonOutputManga = []

    # Get entries from Anime, not in MAL
    if jsonAnime is not None:
        fMain.logString("Checking anime list..", logSrc)
        for entry in jsonAnime:
            # Get each entry
            if (entry["idMal"] < 1):
                # If not in MAL, ID = 0
                statInMAL += 1
                jsonData = {}
                jsonData["idAnilist"] = entry["idAnilist"]
                jsonData["titleEnglish"] = entry["titleEnglish"]
                jsonData["titleRomaji"] = entry["titleRomaji"]
                if str(entry["synonyms"]) == "[]":
                    jsonData["synonyms"] = ""
                else:
                    jsonData["synonyms"] = entry["synonyms"]
                jsonData["format"] = entry["format"]
                jsonData["source"] = entry["source"]
                jsonData["status"] = entry["status"]
                jsonData["startedAt"] = entry["startedAt"]
                jsonData["completedAt"] = entry["completedAt"]
                jsonData["progress"] = entry["progress"]
                jsonData["totalEpisodes"] = entry["totalEpisodes"]
                jsonData["score"] = entry["score"]
                jsonData["notes"] = entry["notes"]
                # Append to JSON object
                jsonOutputAnime.append(jsonData)

            # Stats checker
            statScore = int(entry["score"])
            if (statScore > 0):
                statScoreTotal = statScoreTotal + statScore
                statScoreCount = statScoreCount + 1
            
            # Count entries
            AnilistStatus = str(entry["status"])
            if (AnilistStatus == "COMPLETED"):
                cComplete = cComplete + 1
            elif (AnilistStatus == "PAUSED"):
                cHold = cHold + 1
            elif (AnilistStatus == "CURRENT"):
                cCurrent = cCurrent + 1
            elif (AnilistStatus == "DROPPED"):
                cDrop = cDrop + 1
            elif (AnilistStatus == "PLANNING"):
                cPlan = cPlan + 1
            elif (AnilistStatus == "REPEATING"):
                cCurrent = cCurrent + 1

        # Write 'outputAnime'
        if jsonOutputAnime:
            fMain.createJsonFile(outputAnime, jsonOutputAnime, logSrc)

        # Write stats for Anime
        cTotal = cComplete + cCurrent + cHold + cPlan + cDrop
        fMain.logString("Appending to file (Average Score stats): " + os.path.basename(outputStats), logSrc)
        averageScore = "{:.2f}".format(statScoreTotal/statScoreCount * 10)
        fMain.write_append(outputStats, "Anime stats:\nAverage Score (out of 100): " + averageScore + "\n")
        fMain.write_append(outputStats, "Count:\nCompleted: " + str(cComplete) + "\nCurrently Watching: " + str(cCurrent) + "\nPaused: " + str(cHold) + "\nPlanning: " + str(cPlan) + "\nDropped: " + str(cDrop) + "\n")
        fMain.write_append(outputStats, "\nTotal: " + str(cTotal))
        fMain.write_append(outputStats, "\nAnime Not in MAL: " + str(statInMAL) + "\n")

    # Add Line Break
    fMain.write_append(outputStats, "=========================================\n")
    # Reset vars
    statScoreTotal = 0
    statScoreCount = 0
    statInMAL = 0
    # Reset count
    cTotal = 0
    cCurrent = 0
    cComplete = 0
    cHold = 0
    cDrop = 0
    cPlan = 0

    # For MANGA
    # Get entries from MANGA, not in MAL
    if jsonManga is not None:
        fMain.logString("Checking manga list..", logSrc)
        for entry in jsonManga:
            # Get each entry
            if (entry["idMal"] < 1):
                # If not in MAL, ID = 0
                statInMAL += 1
                jsonData = {}
                jsonData["idAnilist"] = entry["idAnilist"]
                jsonData["titleEnglish"] = entry["titleEnglish"]
                jsonData["titleRomaji"] = entry["titleRomaji"]
                if str(entry["synonyms"]) == "[]":
                    jsonData["synonyms"] = ""
                else:
                    jsonData["synonyms"] = entry["synonyms"]
                jsonData["format"] = entry["format"]
                jsonData["source"] = entry["source"]
                jsonData["status"] = entry["status"]
                jsonData["startedAt"] = entry["startedAt"]
                jsonData["completedAt"] = entry["completedAt"]
                jsonData["progress"] = entry["progress"]
                jsonData["progressVolumes"] = entry["progressVolumes"]
                jsonData["totalChapters"] = entry["totalChapters"]
                jsonData["totalVol"] = entry["totalVol"]
                jsonData["score"] = entry["score"]
                jsonData["notes"] = entry["notes"]
                # Append to JSON object
                jsonOutputManga.append(jsonData)

            # Stats checker
            statScore = int(entry["score"])
            if (statScore > 0):
                statScoreTotal = statScoreTotal + statScore
                statScoreCount = statScoreCount + 1

            # Count entries
            AnilistStatus = str(entry["status"])
            if (AnilistStatus == "COMPLETED"):
                cComplete = cComplete + 1
            elif (AnilistStatus == "PAUSED"):
                cHold = cHold + 1
            elif (AnilistStatus == "CURRENT"):
                cCurrent = cCurrent + 1
            elif (AnilistStatus == "DROPPED"):
                cDrop = cDrop + 1
            elif (AnilistStatus == "PLANNING"):
                cPlan = cPlan + 1
            elif (AnilistStatus == "REPEATING"):
                cCurrent = cCurrent + 1
                
        # Write 'outputManga'
        if jsonOutputManga:
            fMain.createJsonFile(outputManga, jsonOutputManga, logSrc)

        # Write stats for Manga
        cTotal = cComplete + cCurrent + cHold + cPlan + cDrop
        fMain.logString("Appending to file (Average Score stats): " + os.path.basename(outputStats), logSrc)
        averageScore = "{:.2f}".format(statScoreTotal/statScoreCount * 10)
        fMain.write_append(outputStats, "Manga stats:\nAverage Score (out of 100): " + averageScore + "\n")
        fMain.write_append(outputStats, "Count:\nCompleted: " + str(cComplete) + "\nCurrently Reading: " + str(cCurrent) + "\nPaused: " + str(cHold) + "\nPlanning: " + str(cPlan) + "\nDropped: " + str(cDrop) + "\n")
        fMain.write_append(outputStats, "\nTotal: " + str(cTotal))
        fMain.write_append(outputStats, "\nManga Not in MAL: " + str(statInMAL) + "\n")
