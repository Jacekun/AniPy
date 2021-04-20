# Imports
import json
import requests
from datetime import datetime

# Anilist API URL
AnilistURL = 'https://graphql.anilist.co'

# Logger
def logger(text):
    print(f'[{datetime.now().strftime("%H:%M:%S")}][anilist_request]: {text}')

# Return media query string
def queryMedia():
    query = '''
    query ($userID: Int, $MEDIA: MediaType) {
    MediaListCollection (userId: $userID, type: $MEDIA) { 
        lists {
            status
            entries
            {
                status
                completedAt { year month day }
                startedAt { year month day }
                progress
                progressVolumes
                score
                notes
                private
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
                    coverImage { medium }
                    synonyms
                }
            }
        }
    }
    }
    '''
    return query

# Return json query for user ID
def queryUser(userName):
  queryUser = "query ($userName: String) { User (search: $userName) { id } }"
  varUser = { 'userName': "'" + userName + "'" }
  json={'query': queryUser, 'variables': varUser}
  return json

# Return User ID, from Username
def anilist_getUserID(userName):
    logger("Getting User ID from Anilist..")
    try:
        response = requests.post(AnilistURL, json=queryUser(userName))
    except:
        logger("Internet error! Check your connection.")
        return -1

    # If successful, get User ID from Username
    if (response.status_code == 200):
        jsonParsed = json.loads(response.content)
        userID = jsonParsed["data"]["User"]["id"]
        logger("User ID: " + str(userID))
        return userID
    else:
        logger("Cannot get User ID!")
        logger(str(response.content))
        return 0

# Request user media list, returns JSON Object (Authenticated with token)
def anilist_userlist(accessToken, userID, MEDIA = "ANIME"):
    logger("Getting " + MEDIA + " from Anilist..")
    varQuery = { 'userID': str(userID), 'MEDIA' : MEDIA }
    response = requests.post(AnilistURL, json={'query': queryMedia(), 'variables': varQuery}, headers={"Authorization": f"Bearer {accessToken}"})
    if (response.status_code == 200):
        jsonParsed = json.loads(response.content)
        logger(MEDIA + " request success! Returned JSON object..")
        return jsonParsed
    else:
        logger(MEDIA + " Request Error! [Status code: " + str(response.status_code) + "]")
        logger(response.content)
        return None

# Request user media list, returns JSON Object (Public List)
def anilist_userlist_public(userID, MEDIA = "ANIME"):
    logger("Getting " + MEDIA + " from Anilist..")
    varQuery = { 'userID': str(userID), 'MEDIA' : MEDIA }
    response = requests.post(AnilistURL, json={'query': queryMedia(), 'variables': varQuery})
    if (response.status_code == 200):
        jsonParsed = json.loads(response.content)
        logger(MEDIA + " request success! Returned JSON object..")
        return jsonParsed
    else:
        logger(MEDIA + " Request Error! [Status code: " + str(response.status_code) + "]")
        logger(response.content)
        return None