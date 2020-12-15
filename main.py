# imports
import requests
import json
from os import path

# Define functions
def validateStr(x):
  if x is not None:
    return str(x).replace('"', "'")
  return ""

def validateInt(x):
  if x is not None:
    return str(x)
  return '0'

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
        }
      }
    }
  }
  }
  '''  

  # Get Anime List
  if not (path.exists("anime.json")):
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
        # Iterate over the MediaCollection List
        # Write to file
        f = open("anime.json","a+")
        f.write('[ ')
        f.close()
        for anime in listAnime:
          animeInfo = anime["entries"]
          # Iterate over the anime information, inside the entries
          for entry in animeInfo:
            jsontoAdd = "{ "
            jsontoAdd += '"idAnilist": ' + str(entry["media"]["id"]) + ", "
            jsontoAdd += '"idMal": ' + str(entry["media"]["idMal"]) + ", "
            jsontoAdd += '"titleEnglish": "' + str(entry["media"]["title"]["english"]) + '", '
            jsontoAdd += '"titleRomaji": "' + str(entry["media"]["title"]["romaji"]) + '", '
            jsontoAdd += '"format": "' + str(entry["media"]["format"]) + '", '
            jsontoAdd += '"status": "' + str(entry["status"]) + '", '
            jsontoAdd += '"startedAt": "' + str(entry["startedAt"]["year"]) + "-" + str(entry["startedAt"]["month"]) + "-" + str(entry["startedAt"]["day"]) + '", '
            jsontoAdd += '"completedAt": "' + str(entry["completedAt"]["year"]) + "-" + str(entry["completedAt"]["month"]) + "-" + str(entry["completedAt"]["day"]) + '", '
            jsontoAdd += '"progress": ' + str(entry["progress"]) + ", "
            jsontoAdd += '"progressTotal": ' + str(entry["media"]["episodes"]) + ", "
            jsontoAdd += '"score": ' + str(entry["score"]) + ", "
            jsontoAdd += '"notes": "' + str(entry["notes"]) + '" }, '
            # jsontoAdd += "" + str(entry["media"]["coverImage"]["medium"])

            # Replace 'None" with Zero
            jsontoAdd = jsontoAdd.replace('"progress": None', '"progress": 0')
            jsontoAdd = jsontoAdd.replace('"progressTotal": None', '"progressTotal": 0')
            jsontoAdd = jsontoAdd.replace('"idMal": None', '"idMal": 0')
            jsontoAdd = jsontoAdd.replace('"score": None', '"score": 0')

            # Remove last comma ','
            jsontoAdd = jsontoAdd.replace('}, ]', '} ]')

            # jsonResult += jsontoAdd

            # Write to file
            with open("anime.json","a+", encoding='utf-8') as f:
              f.write(jsontoAdd)

            #break

        # Write to file
        f = open("anime.json","a+")
        f.write('] ')
        f.close()
        
        # Done anime
        print("Done Anime!")

      else:
        print("Anime Request Error! [Status code: " + str(response.status_code) + "]")
        print(response.content)
  else:
    print("anime.json file already exist!")
    
  # Get Manga List
  if not (path.exists("manga.json")):
    varQueryManga = {
        'userID': userID,
        'MEDIA' : 'MANGA'
    }

    response = requests.post(url, json={'query': query, 'variables': varQueryManga})
    if (response.status_code == 200):
      jsonParsed = json.loads(response.content)
      listManga = jsonParsed["data"]["MediaListCollection"]["lists"]
      print("manga list is generated!")
      
      # Write to file
      f = open("manga.json","a+")
      f.write('[ ')
      f.close()

      # Iterate over the MediaCollection List
      for manga in listManga:
        mangaInfo = manga["entries"]
        # Iterate over the manga information, inside the entries
        for entry in mangaInfo:
          jsontoAdd = "{ "
          jsontoAdd += '"idAnilist": ' + str(entry["media"]["id"]) + ", "
          jsontoAdd += '"idMal": ' + validateInt(entry["media"]["idMal"]) + ", "
          jsontoAdd += '"titleEnglish": "' + validateStr(entry["media"]["title"]["english"]) + '", '
          jsontoAdd += '"titleRomaji": "' + validateStr(entry["media"]["title"]["romaji"]) + '", '
          jsontoAdd += '"format": "' + str(entry["media"]["format"]) + '", '
          jsontoAdd += '"status": "' + str(entry["status"]) + '", '
          jsontoAdd += '"startedAt": "' + validateStr(entry["startedAt"]["year"]) + "-" + validateStr(entry["startedAt"]["month"]) + "-" + validateStr(entry["startedAt"]["day"]) + '", '
          jsontoAdd += '"completedAt": "' + validateStr(entry["completedAt"]["year"]) + "-" + validateStr(entry["completedAt"]["month"]) + "-" + validateStr(entry["completedAt"]["day"]) + '", '
          jsontoAdd += '"progress": ' + validateInt(entry["progress"]) + ", "
          jsontoAdd += '"totalChapters": ' + validateInt(entry["media"]["chapters"]) + ", "
          jsontoAdd += '"totalVol": ' + validateInt(entry["media"]["volumes"]) + ", "
          jsontoAdd += '"score": ' + validateInt(entry["score"]) + ", "
          jsontoAdd += '"notes": "' + validateStr(entry["notes"]) + '" }, '

          # Remove last comma ','
          jsontoAdd = jsontoAdd.replace('}, ]', '} ]')

          # Write to file
          with open("manga.json","a+", encoding='utf-8') as f:
            f.write(jsontoAdd)

      # Write to file
      f = open("manga.json","a+")
      f.write('] ')
      f.close()
      
      # Done manga
      print("Done manga!")

    else:
      print("Manga Request Error! [Status code: " + str(response.status_code) + "]")
      print(response.content)
  else:
    print("manga.json file already exist!")