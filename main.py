# imports
import requests
import json

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
  varQueryAnime = {
      'userID': userID,
      'MEDIA' : 'ANIME'
  }

  # Get Anime List
  jsonResult = ""
  response = requests.post(url, json={'query': query, 'variables': varQueryAnime})
  if (response.status_code == 200):
    jsonParsed = json.loads(response.content)
    listAnime = jsonParsed["data"]["MediaListCollection"]["lists"]
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
        f = open("anime.json","a+")
        f.writelines(jsontoAdd)
        f.close()

        break
      #break
    # Write to file
    f = open("anime.json","a+")
    f.write('] ')
    f.close()
      
  else:
    print("Anime Request Error! [Status code: " + str(response.status_code) + "]")
    print(response.content)