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
  response = requests.post(url, json={'query': query, 'variables': varQueryAnime})
  if (response.status_code == 200):
    jsonParsed = json.loads(response.content)
    listAnime = jsonParsed["data"]["MediaListCollection"]["lists"]
    # Iterate over the MediaCollection List
    for anime in listAnime:
      animeInfo = anime["entries"]
      # Iterate over the anime information, inside the entries
      for entry in animeInfo:
        print("--------------------------------------------------")
        print("ID: " + str(entry["media"]["id"]))
        print("Title: " + str(entry["media"]["title"]["english"]))
        print("Romaji: " + str(entry["media"]["title"]["romaji"]))
        print("Format: " + str(entry["media"]["format"]))
        print("Status" + str(entry["status"]) + ": ")
        print("StartedAt: " + str(entry["startedAt"]["year"]))
        print("CompletedAt: " + str(entry["completedAt"]["year"]))
        print("Progress: " + str(entry["progress"]) + "/" + str(entry["media"]["episodes"]))
        print("Progress Vols: " + str(entry["progressVolumes"]))
        print("Score: " + str(entry["score"]))
        print("Notes: " + str(entry["notes"]))
        print(str(entry["media"]["coverImage"]["medium"]))
        break
      #break
  else:
    print("Anime Request Error! [Status code: " + str(response.status_code) + "]")
    print(response.content)