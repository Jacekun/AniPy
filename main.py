# imports
import requests
import json
import os

# Define functions
# Check if not Null, and return
def validateStr(x):
  if x is not None:
    return str(x).replace('"', "'")
  return ""
# Check if not Null, and return
def validateInt(x):
  if x is not None:
    return str(x)
  return '0'
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
  return "<" + name + "><![CDATA[" + content + "]]></" + name + ">"
def toMalval(content, name):
  return "<" + name + ">" + content + "</" + name + ">"
def toMaldate(year, month, day):
  date = validateDate(year, month, day)
  if (date == ""):
    return "0000-00-00"
  return date
def toMalMangaStatus(status):
  malstatus = validateStr(status)
  if (malstatus == "COMPLETED"):
    return "Completed"
  elif (malstatus == "PAUSED"):
    return "On-Hold"
  elif (malstatus == "CURRENT"):
    return "Reading"
  elif (malstatus == "DROPPED"):
    return "Dropped"
  elif (malstatus == "PLANNING"):
    return "Plan to Read"
  else:
    return ""
# Add texts on beginning of file
def line_prepender(filename, line):
    with open(filename, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line + '\n' + content)

# Anilist API URL
url = 'https://graphql.anilist.co'

# Get Username
userName = input("Enter your Anilist Username: ")

# Query for User ID
queryUser = '''
query ($userName: String) { User (search: $userName)
	{
		id
	}
}
'''
varUser = {
  'userName': "'" + userName + "'"
}

# Get USER ID, from USERNAME
response = requests.post(url, json={'query': queryUser, 'variables': varUser})
if (response.status_code == 200):
  jsonParsed = json.loads(response.content)
  userID = jsonParsed["data"]["User"]["id"]
  print("User ID: " + str(userID))
else:
  print("Cannot get User!")
  print(response.content)
  userID = 0

if userID > 0:
  # Query for Anime
  query = '''
  query ($userID: Int, $MEDIA: MediaType) {
  MediaListCollection (userId: $userID, type: $MEDIA) { 
    lists {
      status
      entries
      {
        status
        completedAt {
          year
          month
          day
        }
        startedAt {
          year
          month
          day
        }
        progress
        progressVolumes
        score
        notes
        media
        {
          id
          idMal
          season
          seasonYear
          format
          source
          episodes
          chapters
          volumes
          title
          {
            english
            romaji
          }
          description
          coverImage
          {
            medium
          }
          synonyms
        }
      }
    }
  }
  }
  '''  

  # Get Anime List
  outputAnime = "anime.json"
  if not (os.path.exists(outputAnime)):
      varQueryAnime = {
          'userID': userID,
          'MEDIA' : 'ANIME'
      }

      # jsonResult = ""
      response = requests.post(url, json={'query': query, 'variables': varQueryAnime})
      if (response.status_code == 200):
        jsonParsed = json.loads(response.content)
        listAnime = jsonParsed["data"]["MediaListCollection"]["lists"]
        print("anime list is generated!")
        
        # Write to file
        f = open(outputAnime,"a+")
        f.write('[ ')
        f.close()

        # Iterate over the MediaCollection List
        for anime in listAnime:
          animeInfo = anime["entries"]
          # Iterate over the anime information, inside the entries
          for entry in animeInfo:
            jsontoAdd = "{ "
            jsontoAdd += '"idAnilist": ' + str(entry["media"]["id"]) + ", "
            jsontoAdd += '"idMal": ' + validateInt(entry["media"]["idMal"]) + ", "
            jsontoAdd += '"titleEnglish": "' + validateStr(entry["media"]["title"]["english"]) + '", '
            jsontoAdd += '"titleRomaji": "' + validateStr(entry["media"]["title"]["romaji"]) + '", '
            jsontoAdd += '"synonyms": "' + validateStr(entry["media"]["synonyms"]) + '", '
            jsontoAdd += '"format": "' + validateStr(entry["media"]["format"]) + '", '
            jsontoAdd += '"source": "' + validateStr(entry["media"]["source"]) + '", '
            jsontoAdd += '"status": "' + validateStr(entry["status"]) + '", '
            jsontoAdd += '"startedAt": "' + validateDate(entry["startedAt"]["year"], entry["startedAt"]["month"], entry["startedAt"]["day"]) + '", '
            jsontoAdd += '"completedAt": "' + validateDate(entry["completedAt"]["year"], entry["completedAt"]["month"], entry["completedAt"]["day"]) + '", '
            jsontoAdd += '"progress": ' + validateInt(entry["progress"]) + ", "
            jsontoAdd += '"progressTotal": ' + validateInt(entry["media"]["episodes"]) + ", "
            jsontoAdd += '"score": ' + validateInt(entry["score"]) + ", "
            jsontoAdd += '"notes": "' + validateStr(entry["notes"]) + '" }, '
            # jsontoAdd += "" + str(entry["media"]["coverImage"]["medium"])

            # Write to file
            with open(outputAnime,"a+", encoding='utf-8') as f:
              f.write(jsontoAdd)

        # Delete last comma ','
        with open(outputAnime, 'rb+') as filehandle:
          filehandle.seek(-2, os.SEEK_END)
          filehandle.truncate()

        # Write to file
        with open(outputAnime,"a+") as f:
          f.write(']')
        
        # Done anime
        print("Done! File generated: " + outputAnime)

      else:
        print("Anime Request Error! [Status code: " + str(response.status_code) + "]")
        print(response.content)
  else:
    print("anime.json file already exist!")
    
  # Get Manga List
  outputManga = "manga.json"
  xmlManga = "manga.xml"
  if not (os.path.exists(outputManga)):
    varQueryManga = {
        'userID': userID,
        'MEDIA' : 'MANGA'
    }

    response = requests.post(url, json={'query': query, 'variables': varQueryManga})
    if (response.status_code == 200):
      jsonParsed = json.loads(response.content)
      listManga = jsonParsed["data"]["MediaListCollection"]["lists"]
      print("manga list is generated!")
      
      # Write to json file
      with open(outputManga, "a+", encoding='utf-8') as f:
        f.write('[\n')

      # Count Manga entries
      cTotal = 0
      cRead = 0
      cComplete = 0
      cHold = 0
      cDrop = 0
      cPtr = 0

      # Iterate over the MediaCollection List
      for manga in listManga:
        mangaInfo = manga["entries"]
        # Iterate over the manga information, inside the entries
        for entry in mangaInfo:
          jsontoAdd = "\t{\n"
          # ID
          jsontoAdd += '\t\t"idAnilist": ' + str(entry["media"]["id"]) + ",\n"
          malID = validateInt(entry["media"]["idMal"])
          jsontoAdd += '\t\t"idMal": ' + malID + ",\n"
          # Titles
          jsontoAdd += '\t\t"titleEnglish": "' + validateStr(entry["media"]["title"]["english"]) + '",\n'
          jsontoAdd += '\t\t"titleRomaji": "' + validateStr(entry["media"]["title"]["romaji"]) + '",\n'
          jsontoAdd += '\t\t"synonyms": "' + validateStr(entry["media"]["synonyms"]) + '",\n'
          # Format and Source
          jsontoAdd += '\t\t"format": "' + validateStr(entry["media"]["format"]) + '",\n'
          jsontoAdd += '\t\t"source": "' + validateStr(entry["media"]["source"]) + '",\n'
          # Status and dates
          jsontoAdd += '\t\t"status": "' + validateStr(entry["status"]) + '",\n'
          jsontoAdd += '\t\t"startedAt": "' + validateDate(entry["startedAt"]["year"], entry["startedAt"]["month"], entry["startedAt"]["day"]) + '",\n'
          jsontoAdd += '\t\t"completedAt": "' + validateDate(entry["completedAt"]["year"], entry["completedAt"]["month"], entry["completedAt"]["day"]) + '",\n'
          # Progress
          jsontoAdd += '\t\t"progress": ' + validateInt(entry["progress"]) + ',\n'
          jsontoAdd += '\t\t"progressVolumes": ' + validateInt(entry["progressVolumes"]) + ",\n"
          jsontoAdd += '\t\t"totalChapters": ' + validateInt(entry["media"]["chapters"]) + ",\n"
          jsontoAdd += '\t\t"totalVol": ' + validateInt(entry["media"]["volumes"]) + ",\n"
          # Others
          jsontoAdd += '\t\t"score": ' + validateInt(entry["score"]) + ",\n"
          jsontoAdd += '\t\t"notes": "' + validateStr(entry["notes"]) + '"\n\t},\n'

          # Write to json file
          with open(outputManga,"a+", encoding='utf-8') as f:
            f.write(jsontoAdd)

          # Write to MAL Xml File
          if malID != '0':
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
            xmltoWrite += "\t\t" + toMalval(toMalMangaStatus(entry["status"]), 'my_status') + '\n'
            xmltoWrite += "\t\t" + toMalstr(validateStr(entry["notes"]), 'my_comments') + '\n'
            xmltoWrite += "\t\t" + toMalval('0', 'my_times_read') + '\n'
            xmltoWrite += "\t\t" + toMalstr('', 'my_tags') + '\n'
            xmltoWrite += "\t\t" + toMalval('', 'my_reread_value') + '\n'
            xmltoWrite += "\t\t" + toMalval('1', 'update_on_import') + '\n'
            xmltoWrite += "\t</manga>\n"

            # Add count
            malstatus = validateStr(entry["status"])
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

            # Write to file
            with open(xmlManga,"a+", encoding='utf-8') as f:
              f.write(xmltoWrite)

      # Delete last comma ',', in json file
      with open(outputManga, 'rb+') as filehandle:
        filehandle.seek(-3, os.SEEK_END)
        filehandle.truncate()

      # Write ']' at the end, to json file
      with open(outputManga,"a+") as f:
        f.write('\n]')
      
      # Write to MAL xml file
      with open(xmlManga,"a+", encoding='utf-8') as f:
        f.write('</myanimelist>')

      # Total counts
      cTotal = cRead + cComplete + cHold + cDrop + cPtr

      malprepend = '<?xml version="1.0" encoding="UTF-8" ?>\n<myanimelist>\n'
      malprepend += '\t<myinfo>\n'
      malprepend += '\t\t' + toMalval('', 'user_id') + '\n'
      malprepend += '\t\t' + toMalval(userName, 'user_name') + '\n'
      malprepend += '\t\t' + toMalval('2', 'user_export_type') + '\n'
      malprepend += '\t\t' + toMalval(str(cTotal), 'user_total_manga') + '\n'
      malprepend += '\t\t' + toMalval(str(cRead), 'user_total_reading') + '\n'
      malprepend += '\t\t' + toMalval(str(cComplete), 'user_total_completed') + '\n'
      malprepend += '\t\t' + toMalval(str(cHold), 'user_total_onhold') + '\n'
      malprepend += '\t\t' + toMalval(str(cDrop), 'user_total_dropped') + '\n'
      malprepend += '\t\t' + toMalval(str(cPtr), 'user_total_plantoread') + '\n'
      malprepend += '\t</myinfo>\n'
      line_prepender(xmlManga, malprepend)

      # Done manga
      print("Done! File generated: " + outputManga)
      print("Done! File generated: " + xmlManga)

    else:
      print("Manga Request Error! [Status code: " + str(response.status_code) + "]")
      print(response.content)
  else:
    print("manga.json file already exist!")