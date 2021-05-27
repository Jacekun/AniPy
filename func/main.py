# Global functions (Main functions)
# Imports
import os
from datetime import datetime
import json
# 
print(f'[{datetime.now().strftime("%H:%M:%S")}][]: Imported func.main')

# Log string, and return it
def logString(text, source="main"):
  print(f'[{datetime.now().strftime("%H:%M:%S")}][{source}]: {text}')
  return text

# Check if not Null, and return
def validateStr(x):
  if x is not None:
    #fixed = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', str(x))
    #fixed = str(x).replace('\\', "\\\\") # Allow 'Escape backslash' to be encoded
    #return fixed.replace('"', "'") # Replace double quotes to single quote
    return str(x)
  return ""

# Check if array is null, and return empty string
def validateStrArr(x):
  text = validateStr(x)
  if text == "[]":
    return ""
  return text

# Check if not Null, and return
def validateInt(x):
  if x is not None:
    if (x > 0):
      return str(x)
    return '0'
  return '0'

def validateIntAsInt(x):
  if x is not None:
    if (x > 0):
      return x
    return 0
  return 0

# Check if not Null, and return
def validateDate(year, month, day):
  date = validateStr(year) + "-" + validateStr(month) + "-" + validateStr(day)
  if (date == "--"):
    return ""
  else:
    dateArr = date.split('-')
    if len(dateArr[1]) < 2:
      dateArr[1] = '0' + dateArr[1]
    if len(dateArr[2]) < 2:
      dateArr[2] = '0' + dateArr[2]
    date = dateArr[0] + '-' + dateArr[1] + '-' + dateArr[2]
  return date

# Create string/int for MAL XML file
def toMalstr(content, name):
  fixed = validateStr(content)
  return "<" + name + "><![CDATA[" + fixed + "]]></" + name + ">"

def toMalval(content, name):
  return "<" + name + ">" + content + "</" + name + ">"

def toMaldate(year, month, day):
  date = validateDate(year, month, day)
  if (date == ""):
    return "0000-00-00"
  return date

def toMalStatus(status, media):
  AnilistStatus = validateStr(status)
  if (AnilistStatus == "COMPLETED"):
    return "Completed"
  elif (AnilistStatus == "PAUSED"):
    return "On-Hold"
  elif (AnilistStatus == "CURRENT"):
    if (media == 'anime'):
      return "Watching"
    else:
      return "Reading"
  elif (AnilistStatus == "DROPPED"):
    return "Dropped"
  elif (AnilistStatus == "PLANNING"):
    if (media == 'anime'):
      return "Plan to Watch"
    else:
      return "Plan to Read"
  elif (AnilistStatus == "REPEATING"):
    if (media == 'anime'):
      return "Watching"
    else:
      return "Reading"
  else:
    return ""

# Add texts on beginning of file
def line_prepender(filename, line):
    with open(filename, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line + '\n' + content)

# Write 'contents' to end of file (append string to file)
def write_append(filename, content):
  with open(filename, "a+", encoding='utf-8') as f:
    f.write(content)
    
# Remove characters from end of file
def write_remove(filename, char_count):
  with open(filename, 'rb+') as filehandle:
    filehandle.seek(-char_count, os.SEEK_END)
    filehandle.truncate()

# Return json dict object to be appended
def entry_json(entry, mediaType):
  jsonObj = {}
  # ID
  jsonObj["idAnilist"] = validateIntAsInt(entry["media"]["id"])
  malID = validateIntAsInt(entry["media"]["idMal"])
  jsonObj["idMal"] = malID
  # Titles
  jsonObj["titleEnglish"] = validateStr(entry["media"]["title"]["english"])
  jsonObj["titleRomaji"] = validateStr(entry["media"]["title"]["romaji"])
  jsonObj["synonyms"] = validateStrArr(entry["media"]["synonyms"])
  # Format and Source
  jsonObj["format"] = validateStr(entry["media"]["format"])
  jsonObj["source"] = validateStr(entry["media"]["source"])
  # Status and dates
  jsonObj["status"] = validateStr(entry["status"])
  jsonObj["startedAt"] = validateDate(entry["startedAt"]["year"], entry["startedAt"]["month"], entry["startedAt"]["day"])
  jsonObj["completedAt"] = validateDate(entry["completedAt"]["year"], entry["completedAt"]["month"], entry["completedAt"]["day"])
  # Progress
  jsonObj["progress"] = validateIntAsInt(entry["progress"])

  if (mediaType == 'ANIME'):
    jsonObj["totalEpisodes"] = validateIntAsInt(entry["media"]["episodes"])
  else:
    jsonObj["progressVolumes"] = validateIntAsInt(entry["progressVolumes"])
    jsonObj["totalChapters"] = validateIntAsInt(entry["media"]["chapters"])
    jsonObj["totalVol"] = validateIntAsInt(entry["media"]["volumes"])
  
  # Others
  jsonObj["score"] = validateIntAsInt(entry["score"])
  jsonObj["private"] = str(entry["private"])
  jsonObj["notes"] = validateStr(entry["notes"])
  return jsonObj

# Return strings to add to json
def entry_json_str(entry, mediaType):
  jsontoAdd = "\t{\n"
  # ID
  jsontoAdd += '\t\t"idAnilist": ' + str(entry["media"]["id"]) + ",\n"
  malID = validateInt(entry["media"]["idMal"])
  jsontoAdd += '\t\t"idMal": ' + malID + ",\n"
  # Titles
  jsontoAdd += '\t\t"titleEnglish": "' + validateStr(entry["media"]["title"]["english"]) + '",\n'
  jsontoAdd += '\t\t"titleRomaji": "' + validateStr(entry["media"]["title"]["romaji"]) + '",\n'
  jsontoAdd += '\t\t"synonyms": "' + validateStrArr(entry["media"]["synonyms"]) + '",\n'
  # Format and Source
  jsontoAdd += '\t\t"format": "' + validateStr(entry["media"]["format"]) + '",\n'
  jsontoAdd += '\t\t"source": "' + validateStr(entry["media"]["source"]) + '",\n'
  # Status and dates
  jsontoAdd += '\t\t"status": "' + validateStr(entry["status"]) + '",\n'
  jsontoAdd += '\t\t"startedAt": "' + validateDate(entry["startedAt"]["year"], entry["startedAt"]["month"], entry["startedAt"]["day"]) + '",\n'
  jsontoAdd += '\t\t"completedAt": "' + validateDate(entry["completedAt"]["year"], entry["completedAt"]["month"], entry["completedAt"]["day"]) + '",\n'
  # Progress
  jsontoAdd += '\t\t"progress": ' + validateInt(entry["progress"]) + ',\n'

  if (mediaType == 'ANIME'):
    jsontoAdd += '\t\t"totalEpisodes": ' + validateInt(entry["media"]["episodes"]) + ",\n"
  else:
    jsontoAdd += '\t\t"progressVolumes": ' + validateInt(entry["progressVolumes"]) + ",\n"
    jsontoAdd += '\t\t"totalChapters": ' + validateInt(entry["media"]["chapters"]) + ",\n"
    jsontoAdd += '\t\t"totalVol": ' + validateInt(entry["media"]["volumes"]) + ",\n"
  
  # Others
  jsontoAdd += '\t\t"score": ' + validateInt(entry["score"]) + ",\n"
  jsontoAdd += '\t\t"private": "' + str(entry["private"]) + '",\n'
  jsontoAdd += '\t\t"notes": "' + validateStr(entry["notes"]) + '"\n\t},\n'
  return jsontoAdd

# Return string to add to MAL XML
def entry_xmlstr(mediaType, malID, entry, status):
  if mediaType == "ANIME":
    xmltoWrite = "\t<anime>\n"
    xmltoWrite += "\t\t" + toMalval(malID, 'series_animedb_id') + '\n'
    xmltoWrite += "\t\t" + toMalstr(validateStr(entry["media"]["title"]["romaji"]), 'series_title') + '\n'
    xmltoWrite += "\t\t" + toMalval('', 'series_type') + '\n'
    xmltoWrite += "\t\t" + toMalval(validateInt(entry["media"]["episodes"]), 'series_episodes') + '\n'
    xmltoWrite += "\t\t" + toMalval('0', 'my_id') + '\n'
    xmltoWrite += "\t\t" + toMalval(validateInt(entry["progress"]), 'my_watched_episodes') + '\n'
    xmltoWrite += "\t\t" + toMalval(toMaldate(entry["startedAt"]["year"],entry["startedAt"]["month"],entry["startedAt"]["day"]), 'my_start_date') + '\n'
    xmltoWrite += "\t\t" + toMalval(toMaldate(entry["completedAt"]["year"],entry["completedAt"]["month"],entry["completedAt"]["day"]), 'my_finish_date') + '\n'
    xmltoWrite += "\t\t" + toMalval('', 'my_rated') + '\n'
    xmltoWrite += "\t\t" + toMalval(validateInt(entry["score"]), 'my_score') + '\n'
    xmltoWrite += "\t\t" + toMalval('', 'my_dvd') + '\n'
    xmltoWrite += "\t\t" + toMalval('', 'my_storage') + '\n'
    xmltoWrite += "\t\t" + toMalval(toMalStatus(entry["status"], 'anime'), 'my_status') + '\n'
    xmltoWrite += "\t\t" + toMalstr(validateStr(entry["notes"]), 'my_comments') + '\n'
    xmltoWrite += "\t\t" + toMalval('0', 'my_times_watched') + '\n'
    xmltoWrite += "\t\t" + toMalval('', 'my_rewatch_value') + '\n'
    xmltoWrite += "\t\t" + toMalstr('', 'my_tags') + '\n'
    if (status=="REPEATING"):
      xmltoWrite += "\t\t" + toMalval('YES', 'my_rewatching') + '\n'
    else:
      xmltoWrite += "\t\t" + toMalval('NO', 'my_rewatching') + '\n'
    xmltoWrite += "\t\t" + toMalval('0', 'my_rewatching_ep') + '\n'
    xmltoWrite += "\t\t" + toMalval('1', 'update_on_import') + '\n'
    xmltoWrite += "\t</anime>\n"
  else:
    xmltoWrite = "\t<manga>\n"
    xmltoWrite += "\t\t" + toMalval(malID, 'manga_mangadb_id') + '\n'
    xmltoWrite += "\t\t" + toMalstr(validateStr(entry["media"]["title"]["romaji"]), 'manga_title') + '\n'
    xmltoWrite += "\t\t" + toMalval(validateInt(entry["media"]["volumes"]), 'manga_volumes') + '\n'
    xmltoWrite += "\t\t" + toMalval(validateInt(entry["media"]["chapters"]), 'manga_chapters') + '\n'
    xmltoWrite += "\t\t" + toMalval('', 'my_id') + '\n'
    xmltoWrite += "\t\t" + toMalval(validateInt(entry["progressVolumes"]), 'my_read_volumes') + '\n'
    xmltoWrite += "\t\t" + toMalval(validateInt(entry["progress"]), 'my_read_chapters') + '\n'
    xmltoWrite += "\t\t" + toMalval(toMaldate(entry["startedAt"]["year"],entry["startedAt"]["month"],entry["startedAt"]["day"]), 'my_start_date') + '\n'
    xmltoWrite += "\t\t" + toMalval(toMaldate(entry["completedAt"]["year"],entry["completedAt"]["month"],entry["completedAt"]["day"]), 'my_finish_date') + '\n'
    xmltoWrite += "\t\t" + toMalstr('', 'my_scanalation_group') + '\n'
    xmltoWrite += "\t\t" + toMalval(validateInt(entry["score"]), 'my_score') + '\n'
    xmltoWrite += "\t\t" + toMalval('', 'my_storage') + '\n'
    xmltoWrite += "\t\t" + toMalval(toMalStatus(entry["status"], 'manga'), 'my_status') + '\n'
    xmltoWrite += "\t\t" + toMalstr(validateStr(entry["notes"]), 'my_comments') + '\n'
    xmltoWrite += "\t\t" + toMalval('0', 'my_times_read') + '\n'
    xmltoWrite += "\t\t" + toMalstr('', 'my_tags') + '\n'
    xmltoWrite += "\t\t" + toMalval('', 'my_reread_value') + '\n'
    if (status=="REPEATING"):
      xmltoWrite += "\t\t" + toMalval('YES', 'my_rereading') + '\n'
    else:
      xmltoWrite += "\t\t" + toMalval('NO', 'my_rereading') + '\n'
    xmltoWrite += "\t\t" + toMalval('1', 'update_on_import') + '\n'
    xmltoWrite += "\t</manga>\n"
  return xmltoWrite

# Delete file
def deleteFile(file):
    if os.path.exists(file):
        os.remove(file)

# Dump object to json file
def dumpToJson(objToDump, filePath):
  try:
    with open(filePath, "w+", encoding='utf-8') as F:
      F.write(json.dumps(objToDump, ensure_ascii=True, indent=4).encode('utf8').decode())
      return True
  except:
    return False

def createJsonFile(filepath, jsonObject, logSrc = "main"):
  logString("Writing to file " + os.path.basename(filepath), logSrc)
  try:
    with open(filepath, "w+", encoding='utf-8') as F:
        F.write(json.dumps(jsonObject, ensure_ascii=False, indent=4).encode('utf8').decode())
        logString("File generated: " + filepath, logSrc)
  except:
    logString(f"Cannot write json file: {filepath}", logSrc)