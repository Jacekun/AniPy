# AniPy

Create Local backup of anime/manga list from [Anilist.co](https://anilist.co/).

[**View Project History**](doc/VERSION.md) <br>

[**Click to Download Latest Release**](https://github.com/Jacekun/AniPy/releases/download/v1.0.0.0/AniPy_v1.0.0.0.zip)

**Download count :** <br> [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.0.0.0/total.svg)]() <br>

# How to use?

1. Extract downloaded **zipped** file.
2. Run '**main_win.exe**'.
3. Input your **Anilist Username**, and Click **Export** button.

**Note: It would take a long time to fetch the data. Wait for it to finish..** <br>

# Requirements:
  - Windows 64-bit.
  - 3GB RAM, or higher.

# Features:
- Export User Anime/Manga list to JSON file.
- Export User Anime/Manga list to [MAL](https://myanimelist.net/) Xml export file (Can be imported to [MyAnimeList](https://myanimelist.net/import.php)).
- Graphical User Interface, for easy use.

## Files created:

1. **anime.json** / **manga.json** :   Local backup of User [Anilist.co](https://anilist.co/).
2. **anime.xml** / **manga.xml**   :   [MyAnimeList](https://myanimelist.net/) XML export. Can be [imported into MAL](https://myanimelist.net/import.php).  

# Developer

## Packages used

### Import (Included in Python 3.x)
[os](https://docs.python.org/3/library/os.html) <br>
[sys](https://docs.python.org/3/library/sys.html) <br>
[json](https://docs.python.org/3/library/json.html) <br>
[tkinter](https://docs.python.org/3/library/tkinter.html) <br>
[datetime](https://docs.python.org/3/library/datetime.html) <br>

### Install, then Import
[importlib](https://pypi.org/project/importlib/) <br>
[requests](https://pypi.org/project/requests/) <br>
[pygubu](https://pypi.org/project/pygubu/) <br>

## Files:

**[main.py](main.py)** : Console version of App. <br>
**[main_win.py](main_win.py)** : Windows GUI version, using *Pygubu*. <br>
**[main_win.ui](main_win.ui)**     : UI file used. Can be viewed/edited in *[Pygubu-designer](https://pypi.org/project/pygubu-designer/)*. <br>
**[build.cmd](build.cmd)**   : Command line script to build Windows GUI. *Requires 'Pygubu' and 'Pygubu-designer'*. <br>
**[dependencies.txt](dependencies.txt)**    : List of packages required. <br>

**[func / func.py](func/func.py)**    : Main functions. <br>
**[func / anilist_request.py](func/anilist_request.py)**    : Requests to [Anilist.co](https://anilist.co/). <br>