# v1.2.0.0 - Improvements
**Download count :** [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.1.0.0/total.svg)]() <br>

**New:**
- Added "Rereading" Manga to MAL Manga XML file.
- Handles "Rewatching / Rereading", saves it as "Watching / Reading".
- Added script to get Entries which does not exist on MAL. (*Output File:* **anime_NotInMal.json / manga_NotInMal.json**).
- Get **'Average Score'** and **'Anime/Manga count for Each status'**. (*Output File:* **'animemanga_stats.txt'**).

**Inside the Code:**
- Script file for Generating lists of Entries not in MAL. Also, gets stats. (*File:* **'trim_list.py'**).
- Convert 'response.content' on 'anilist_request.py' to string, for proper error-logging.
- Code cleanups.

<br>

# v1.1.0.0 - Re-write
**Download count :** [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.1.0.0/total.svg)]() <br>

**Fixes:**
- Removed duplicate entries from List.

**Inside the Code:**
- Rewritten the Code, making the functions outside of the Main script.
- Added Logger function, with Current Time.

<br>

# v1.0.0.0 - First Version
**Download count :** [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.0.0.0/total.svg)]() <br>

**Features:**
- Export User Anime/Manga list to JSON file.
- Export User Anime/Manga list to [MAL](https://myanimelist.net/) Xml export file (Can be imported to [MyAnimeList](https://myanimelist.net/import.php)).
- Graphical User Interface, for easy use.