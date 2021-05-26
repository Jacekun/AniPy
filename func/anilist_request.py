# Imports
import json
import requests
# Local import
from func.main import logString as logMain

# Anilist API URL
AnilistURL = 'https://graphql.anilist.co'

logMain("Imported func.anilist_request", "")

# Logger
def logger(text):
    logMain(text, "anilist_request")

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
    
# Request access token, using code
def request_accesstkn(ANICLIENT, ANISECRET, REDIRECT_URL, code):
    body = {
        'grant_type': 'authorization_code',
        'client_id': ANICLIENT,
        'client_secret': ANISECRET,
        'redirect_uri': REDIRECT_URL,
        'code': code
    }
    try:
        accessToken = requests.post("https://anilist.co/api/v2/oauth/token", json=body).json().get("access_token")
    except:
        accessToken = None
    return accessToken