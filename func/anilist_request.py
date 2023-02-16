# Imports
import os
import json
import requests
import webbrowser
# Local import
from func.main import logString as logMain
from func.main import inputX as inputX

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
                score(format: POINT_10)
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
                    isAdult
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
    
# Return User ID, from Access Token
def anilist_getUserID_auth(accessToken):
    try:
        resultUserID = requests.post("https://graphql.anilist.co", headers={"Authorization": f"Bearer {accessToken}"}, json={"query": "{Viewer{id}}"}).json()
        userID = resultUserID["data"]["Viewer"]["id"]
        return userID
    except:
        return None

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

# Request public code
def request_pubcode(ANICLIENT, REDIRECT_URL):
    # Get OAuth and Access Token
    logger("Login Anilist on browser, and Authorize AniPy")
    url = f"https://anilist.co/api/v2/oauth/authorize?client_id={ANICLIENT}&redirect_uri={REDIRECT_URL}&response_type=code"
    webbrowser.open(url)

    code = inputX("Paste your token code here (Copied from Anilist webpage result): ", "")
    return code

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
        #logger("Access Token: [" + accessToken + "]")
    except:
        accessToken = None
    return accessToken

# Setup Anilist config
def setup_config(anilistConfig):
    ANICLIENT = ""
    ANISECRET = ""
    REDIRECT_URL = ""
    useOAuth = False

    if not os.path.exists(anilistConfig):
        while not ANICLIENT:
            ANICLIENT = inputX("Enter your Client ID: ", None)
        while not ANISECRET:
            ANISECRET = inputX("Enter your Client Secret: ", None)

        anilistConfigJson = {
        "aniclient" : ANICLIENT,
        "anisecret" : ANISECRET,
        "redirectUrl" : "https://anilist.co/api/v2/oauth/pin"
        }

        with open(anilistConfig, "w+", encoding='utf-8') as F:
            F.write(json.dumps(anilistConfigJson, ensure_ascii=False, indent=4).encode('utf8').decode())
    
    try:
      with open(anilistConfig) as f:
        configData = json.load(f)
      ANICLIENT = configData['aniclient']
      ANISECRET = configData['anisecret']
      REDIRECT_URL = configData['redirectUrl']
      # fMain.logger("\nClient: " + ANICLIENT + "\nSecret: " + ANISECRET)
      useOAuth = True
    except:
      logger(f"There's no correct {anilistConfig} file!")
      useOAuth = False
      
    return useOAuth, ANICLIENT, ANISECRET, REDIRECT_URL
