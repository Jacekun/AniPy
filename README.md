# AniPy

Create local backup of anime/manga list from [Anilist.co](https://anilist.co/).

![GitHub release](https://img.shields.io/github/v/release/Jacekun/AniPy?sort=semver&style=for-the-badge)

| [**View Project History**](doc/VERSION.md) | [**Contribute to AniPy**](CONTRIBUTING.md) | [**Report Issues**](ISSUE.md) |
|--------------------------------------------|--------------------------------------------|-------------------------------|

# Features:
- Export User Anime/Manga list to JSON file.
- Export User Anime/Manga list to [MyAnimeList](https://myanimelist.net/) XML export file (Can be imported to [MyAnimeList](https://myanimelist.net/import.php)).
- Uses Authentication to Fetch private lists.
- Compare against Tachiyomi backup, and lists all entries not on your library.
- Create Tachiyomi backup file containing Anilist entries not on your library. (*Skips COMPLETED AND DROPPED*)
- Separate NSFW entries. Create files with prefix **'nsfw_'**.

# Limitations:
- Cannot get full information from **"Re-watches / Re-reads"**.
- Cannot cherry-pick entries. (*Planned feature*)

# Output files:
1. **anime.json** / **manga.json** :   Local backup of User [Anilist.co](https://anilist.co/).
2. **anime.xml** / **manga.xml**   :   [MyAnimeList](https://myanimelist.net/) XML export. Can be [imported into MAL](https://myanimelist.net/import.php).  
3. **anime_NotInMal.json** / **manga_NotInMal.json**  : Entries not existing on MAL.
4. **animemanga_stats.txt** : Save Entries' stats. (Average score, Watch/Read count, etc..).
5. **manga_NotInTachi.json** : Anilist manga entries not on your Tachiyomi library.
6. **manga_TachiyomiBackup.json** : Tachiyomi backup file which contains Anilist entries not on your Tachiyomi library. Import it to your Tachiyomi, and Migrate each entries from **'Anilist'** category to appropriate sources.

# Requirements:
- Python 3.9
- 2GB RAM, or higher.
- Stable internet connection.

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
  - Alternatively, you can directly run 1 of the script modes to input the credentials.

# Usage:
## 'Easy' mode
1. Navigate to folder where you saved the source code.
2. Run **[main.py](main.py)**, with command: ``python main.py``.
3. Follow on-screen instructions.

## 'Advanced' mode
1. Run command using: ``python anipy.py -[parameters] --[switches]``

### Parameters:
- ``-user "<type_here>"`` -> Anilist username, if using 'Public Lists Mode'.
- ``-mal "<type_here>"`` -> MyAnimeList username. Will export XML file if provided.
- ``-tachi "<full_filepath>"`` -> Full filepath where Tachiyomi backup file is located.

### Switches:
- ``--a`` -> Use Authentication to fetch for lists. Disregards the ``-user`` parameter.
- ``--t`` -> Trim lists, showing which entries are not on MAL. Also, write stats to file.
- ``--n`` -> Separate NSFW entries on generating output files. Creates files with prefix **'nsfw_'**.
- ``--c`` -> Clear existing output files.
- ``--m`` -> Use **Anilist** as **MAL** username, if **MAL** username is not provided.

### Sample command:
1. Backup all ANIME and MANGA using Authenticated Mode:

```bash
python anipy.py --a
```
2. Backup all ANIME and MANGA using Public Mode:
```bash
python anipy.py -user Jace
```

3. Trim current list and export Tachiyomi backup:
```bash
python anipy.py -tachi "D:\Tachi\backup.proto.gz" --t
```

# Scripts and Files:
## Main scripts:
**[anipy.py](anipy.py)** : Advance script, with one-liner command. <br>
**[main.py](main.py)** : Easy-to-follow script. <br>

## External scripts (Modules):
**[func / main.py](func/main.py)**    : Main global functions. <br>
**[func / anilist_getMedia.py](func/anilist_getMedia.py)** : Generate Anime and Manga JSON/XML files with entries from [Anilist.co](https://anilist.co/). <br>
**[func / anilist_request.py](func/anilist_request.py)** : Query Requests to [Anilist.co](https://anilist.co/). <br>
**[func / getNotOnTachi.py](func/getNotOnTachi.py)** : Generates list of Entries not in Tachiyomi library. <br>
**[func / trim_list.py](func/trim_list.py)** : Generate list of Entries not in MAL. Also gets stats. <br>

## Miscellaneous:
**[requirements.txt](requirements.txt)**    : List of packages required. <br>
