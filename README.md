# AniPy

Create local backup of anime/manga list from [Anilist.co](https://anilist.co/).

[**View Project History**](doc/VERSION.md) <br>

# Requirements:
- Python 3.9
- 2GB RAM, or higher.

# Features:
- Export User Anime/Manga list to JSON file.
- Export User Anime/Manga list to [MyAnimeList](https://myanimelist.net/) XML export file (Can be imported to [MyAnimeList](https://myanimelist.net/import.php)).
- Uses Authentication to Fetch private lists.
- Compare against Tachiyomi backup, and lists all entries not on your library.
- Create Tachiyomi backup file containing Anilist entries not on your library. (*Skips COMPLETED AND DROPPED*)

# Limitations:
- Cannot get full information from **"Re-watches / Re-reads"**.

## Output files:
1. **anime.json** / **manga.json** :   Local backup of User [Anilist.co](https://anilist.co/).
2. **anime.xml** / **manga.xml**   :   [MyAnimeList](https://myanimelist.net/) XML export. Can be [imported into MAL](https://myanimelist.net/import.php).  
3. **anime_NotInMal.json** / **manga_NotInMal.json**  : Entries not existing on MAL.
4. **animemanga_stats.txt** : Save Entries' stats. (Average score, Watch/Read count, etc..).
5. **manga_NotInTachi.json** : Anilist manga entries not on your Tachiyomi library.
6. **manga_TachiyomiBackup.json** : Tachiyomi backup file which contains Anilist entries not on your Tachiyomi library. Import it to your Tachiyomi, and Migrate each entries from **'Anilist'** category to appropriate sources.

# Setup:
1. Install required packages (run Command Prompt in the same folder as '*main.py*'): <br>
  ```cmd
  pip3 install -r requirements.txt
  ```
2. Go to Anilist [**Settings** -> **Developer**](https://anilist.co/settings/developer), and click **Create client**.
  - Type whatever in **Name** field, and use ``https://anilist.co/api/v2/oauth/pin`` as **Redirect URL**.
  - Get information from created client and input them in **anilistConfig.json** (Automatically created if not existing, you need to input the credentials).
  - File must contain these lines. *Replace lines with appropriate values*:
```json
{
    "aniclient": "ID",
    "anisecret": "Secret",
    "redirectUrl": "https://anilist.co/api/v2/oauth/pin"
}
```
3. Run **[main.py](main.py)**.

# Scripts and Files:
## Main scripts:
**[main.py](main.py)** : Console version of App. <br>
**[func / main.py](func/main.py)**    : Main global functions. <br>

## External scripts (Modules):
**[func / anilist_getMedia.py](func/anilist_getMedia.py)** : Generate Anime and Manga JSON/XML files with entries from [Anilist.co](https://anilist.co/). <br>
**[func / anilist_request.py](func/anilist_request.py)** : Query Requests to [Anilist.co](https://anilist.co/). <br>
**[func / getNotOnTachi.py](func/getNotOnTachi.py)** : Generates list of Entries not in Tachiyomi library. <br>
**[func / trim_list.py](func/trim_list.py)** : Generate list of Entries not in MAL. Also gets stats. <br>

## Miscellaneous:
**[requirements.txt](requirements.txt)**    : List of packages required. <br>
