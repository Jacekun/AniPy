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
else:
  print("Request Error! Check username or Internet connection.")
  print(response.content)
  userID = 0

if userID > 0:
  # Query for Anime
  queryAnime = '''
  query ($userID: Int) {
  MediaListCollection (userId: $userID, type: ANIME) { 
    lists {
      status
      entries
      {
        media
        {
          id
          idMal
          status
          title
          {
            english
          }
        }
      }
    }
  }
  }
  '''
  varAnime = {
      'userID': userID
  }

  # Get Anime List
  response = requests.post(url, json={'query': queryAnime, 'variables': varAnime})
  if (response.status_code == 200):
    jsonParsed = json.loads(response.content)
    listAnime = jsonParsed["data"]["MediaListCollection"]["lists"]
    # Iterate over the MediaCollection List
    for anime in listAnime:
      animeInfo = anime["entries"]
      # Iterate over the anime information, inside the entries
      for entry in animeInfo:
        print(str(entry["media"]["status"]) + ": " + str(entry["media"]["id"]) + ": " + str(entry["media"]["title"]["english"]))
  
  else:
    print("Request Error! Check username or Internet connection.")
    print(response.content)