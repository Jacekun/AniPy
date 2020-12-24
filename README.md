# AniPy

Create Local backup of anime/manga list from [Anilist.co](https://anilist.co/).

[**View Project History**](doc/VERSION.md) <br>

[**Click to Download Latest Release**](https://github.com/Jacekun/AniPy/releases/download/v1.1.0.0/AniPy_v1.1.0.0.zip)

**Download count :** <br> [![](https://img.shields.io/github/downloads/Jacekun/AniPy/v1.1.0.0/total.svg)]() <br>

# How to use?

1. Extract downloaded **zipped** file.
2. Run '**main_win.exe**'.
3. Input your **Anilist Username**, and Click **Export** button.

**Note: It would take a long time to fetch the data. Wait for it to finish..** <br>

## Files created:

1. **anime.json** / **manga.json** :   Local backup of User [Anilist.co](https://anilist.co/).
2. **anime.xml** / **manga.xml**   :   [MyAnimeList](https://myanimelist.net/) XML export. Can be [imported into MAL](https://myanimelist.net/import.php).  

# Requirements:
  - Windows 64-bit.
  - 3GB RAM, or higher.

# Features:
- Export User Anime/Manga list to JSON file.
- Export User Anime/Manga list to [MyAnimeList](https://myanimelist.net/) XML export file (Can be imported to [MyAnimeList](https://myanimelist.net/import.php)).
- Graphical User Interface, for easy use.

# Limitations:
- Only works on **Public** User Anilist. (No Authentication).
- Cannot get information from **"Re-watches / Re-reads"**.

# Developer

Written in: **Python 3.9** <br>

## Setup:

1. Install *dependency* packages (run Command Prompt in the same folder as '*main.py*'): <br>
  ```cmd
  pip3 install -r packages.txt
  ```
**To build Windows GUI:** <br>
1. Run this file in *Command Prompt* / *Powershell*: **'build.cmd'**.
2. Copy **'main_win.ui'** into **'dist/files/main_win.ui'**.

## Files:

**[main.py](main.py)** : Console version of App. <br>
**[main_win.py](main_win.py)** : Windows GUI version, using *Pygubu*. <br>
**[main_win.ui](main_win.ui)**     : UI file used. Can be viewed/edited in *[Pygubu-designer](https://pypi.org/project/pygubu-designer/)*. <br>
**[build.cmd](build.cmd)**   : Command line script to build Windows GUI. *Requires 'Pygubu' and 'Pygubu-designer'*. <br>
**[packages.txt](packages.txt)**    : List of packages required. <br>

**[func / func.py](func/func.py)**    : Main functions. <br>
**[func / anilist_request.py](func/anilist_request.py)**    : Requests to [Anilist.co](https://anilist.co/). <br>