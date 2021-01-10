# vx.x.x.x - Improvements
**Download count :** [![](https://img.shields.io/github/downloads/Jacekun/AniPy/vx.x.x.x/total.svg)]() <br>

Based from **main.py** version: 1.2.0.8 <br>

**New and Changes:**
- Append *current date* to the output filenames.

**Inside the Code:**
- All output filepaths are declared inside their own modules, instead of inside **'main.py'**.
- Updated logger format.
- Added additional log info.
- Delete previous **'entries.log'**, every run.
- Code cleanups.
****

# v1.2.0.3 - Improvements
**Download count :** [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.2.0.3/total.svg)]() <br>

Based from **main.py** version: 1.2.0.4 <br>

**New:**
- Handles "Rewatching / Rereading", saves it as "Watching / Reading".
- Moved all **'output files'**, from *'root directory'* to *'root/output'* subfolder.
- Added "Rereading" Manga to MAL Manga XML file.
- Added script to get Entries which does not exist on MAL. (*Output File:* **anime_NotInMal.json / manga_NotInMal.json**).
- Get **'Average Score'** and **'Anime/Manga count for Each status'**. (*Output File:* **'animemanga_stats.txt'**).

**Inside the Code:**
- Moved code getting anime / manga entries, to separate modules. (*File:* **'func/anilist_getAnime.py', 'func/anilist_getManga.py'**)
- Script file for Generating lists of Entries not in MAL. Also, gets stats. (*File:* **'func/trim_list.py'**).
- Convert 'response.content' on 'anilist_request.py' to string, for proper error-logging.
- Validated **'synonyms'**. If result is **"[]"**, return *empty string*.
- Renamed module script: **'func.py'** to **'main.py'**.
- Code cleanups.

**Console-only changes:**
- Ask for username, until a valid one is provided.
- Changed **build.cmd**, to include files during **'executable'** build.
- Added **'main_win.spec'**, to provide options during **'executable'** build.
****

# v1.1.0.0 - Re-write
**Download count :** [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.1.0.0/total.svg)]() <br>

**Fixes:**
- Removed duplicate entries from List.

**Inside the Code:**
- Rewritten the Code, making the functions outside of the Main script.
- Added Logger function, with Current Time.
****

# v1.0.0.0 - First Version
**Download count :** [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.0.0.0/total.svg)]() <br>

**Features:**
- Export User Anime/Manga list to JSON file.
- Export User Anime/Manga list to [MAL](https://myanimelist.net/) Xml export file (Can be imported to [MyAnimeList](https://myanimelist.net/import.php)).
- Graphical User Interface, for easy use.