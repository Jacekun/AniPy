# AniPy

Create Local backup of anime/manga list from [Anilist.co](https://anilist.co/).

[**View Project History**](doc/VERSION.md) <br>

# Windows GUI version
[**Click to Download Latest Release**](https://github.com/Jacekun/AniPy/releases/download/v1.2.0.3/AniPy_v1.2.0.3.zip "Windows") <br>
**Download count :** <br> [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.2.0.3/total.svg)]() <br>

1. Extract downloaded **zipped** file.
2. Run '**main_win.exe**'.
3. Input your **Anilist Username**, and Click **Export** button.

**Note: It would take a long time to fetch the data. Wait for it to finish..** <br>
**NOTE: This only works for 'Public' lists. For 'Private' lists, use the console version.** <br>

## Files created:

1. **anime.json** / **manga.json** :   Local backup of User [Anilist.co](https://anilist.co/).
2. **anime.xml** / **manga.xml**   :   [MyAnimeList](https://myanimelist.net/) XML export. Can be [imported into MAL](https://myanimelist.net/import.php).  
3. **anime_NotInMal.json** / **manga_NotInMal.json**  : Entries not existing on MAL.
4. **animemanga_stats.txt** : Save Entries' stats. (Average score, Watch/Read count, etc..).
5. **manga_NotInTachi.json** : Anilist manga entries not on your Tachiyomi library. *Only on Console version.*

# Requirements:
- Python 3.9 *(For console version)*
- Windows 64-bit. *(For executable)*
- 2GB RAM, or higher.

# Features:
- Export User Anime/Manga list to JSON file.
- Export User Anime/Manga list to [MyAnimeList](https://myanimelist.net/) XML export file (Can be imported to [MyAnimeList](https://myanimelist.net/import.php)).
- Graphical User Interface, for easy use. *No longer maintained. Use console version instead.*
- Uses Authentication to Fetch private lists. **Only on Console version.**
- Compare against Tachiyomi backup, and lists all entries not on your library.

# Limitations:
- Cannot get full information from **"Re-watches / Re-reads"**.

# Developer

Written in: **Python 3.9** <br>

## Setup:

1. Install *dependency* packages (run Command Prompt in the same folder as '*main.py*'): <br>
  ```cmd
  pip3 install -r packages.txt
  ```
2. From Anilist Settings, under **Developer**: **Create client**.
  - Get information from created client and input them in **anilist_config.py** (Create this file).
  - File must contain at least these lines:
```python
  aniclient = '' # Client ID
  anisecret = '' # Client Secret
```

## Files:
### Main scripts:
**[main.py](main.py)** : Console version of App. <br>
**[main_win.py](main_win.py)** : Windows GUI version, using *Pygubu*. <br>
### External scripts:
**[func / main.py](func/main.py)**    : Main functions. <br>
**[func / anilist_request.py](func/anilist_request.py)**    : Requests to [Anilist.co](https://anilist.co/). <br>
**[func / trim_list.py](func/trim_list.py)** : Script file for Generating lists of Entries not in MAL. Also, gets stats. <br>
**[func / trim_list.py](func/getNotOnTachi.py)** : Script file for Generating lists of Entries not in Tachiyomi library. <br>
### UI Files:
**[main_win.ui](main_win.ui)**     : UI file used. Can be viewed/edited in *[Pygubu-designer](https://pypi.org/project/pygubu-designer/)*. <br>
### Misc.:
**[main_win.spec](main_win.spec)**  : Pyinstaller options for building the **executable** file, in **dist** subfolder. <br>
**[build.cmd](build.cmd)**   : Command line script to build Windows GUI. *Requires 'Pygubu', 'Pygubu-designer', and 'main_win.spec' file*. <br>
**[packages.txt](packages.txt)**    : List of packages required. <br>
