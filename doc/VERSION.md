# v1.1
## New features:
- Added Manga re-reading status to MAL xml file.

## Fixes and Changes:
- Fixed JSON not encoding ASCII properly. Fixes [Issue #1](https://github.com/Jacekun/AniPy/issues/1)
- Encodes double quotes to JSON, instead of replacing it into single quote.
- Changed List trimming behavior. Now asks user for explicit permission.
- Changed behavior of choosing **'Public'** or **'Authenticated'** mode. The default is now **'Public mode'**.

## Dev changes:
- Re-written imports. Import locally instead of thru importlib.
- Dump json result as a whole, instead of appending to text file for every result.
  - Pro: Ensures valid json result; Properly encodes ASCII; Properly write 'escape' characters.
  - Cons: Uses more RAM; If an exception happens, it doesn't write anything.
- Combined **'anilist_getAnime'** and **'anilist_getManga'** scripts into one: **'anilist_getMedia'**.
- Log imports from **'func'** subfolder.
- Dropped all GUI supports. AniPy is now fully dedicated as an CLI tool.
- Removed unused *imports* from scripts and *packages* from **'requirements.txt'**.

# v1.08
## Fixes and Changes:
- Clarify that only Legacy version backup of Tachiyomi is accepted.
- Create **'anilistConfig.json'** file, if it does not exist. Needs to enter client Id and secret.
- Use same format as logging when accepting inputs from user.

# v1.07
## New features:
- Create 'output' folder when not existing.
- [WIP] New UI for the script, built using PySide6 and QtDesigner.
  - **Note: Currently, only 'Simple Mode' is working. 'Advance Mode' is still WIP.**

## Fixes and Changes:
- Fix: Only use Tachiyomi compare script when file is not None/null.
- Refactored code for better flow and execution.
- Load anilist config, only when its the mode used.
- Renamed **'packages.txt'** to **'requirements.txt'** following Github standard.
- Correct some log messages.
- Removed unused variables.
- Removed download count from this file.

# v1.06
**This lists all changes after the last Executable update** <br>
## New features:
- Use Authentication to fetch private lists from user.
- Compare list to Tachiyomi library backup and generate json file to be imported to Tachiyomi.
- Use **Press <Enter> key to Exit..** upon process done.
- Count entries from Anilist not in MyAnimeList and export to **'animemanga_stats.txt'**.
- Count total entries and export to **'animemanga_stats.txt'**.
- Toggle use of Authenticated lists and Public list.

## Changes: 
- Use JSON file: **'anilistConfig.json'** to store Anilist config.
- Append *current date* to the output filenames.
- All output filepaths are declared inside their own modules, instead of inside **'main.py'**.
- Pass global path to modules.
- Delete previous **'entries.log'**, every run.
- Updated **'packages.txt'** to match required *imports*.
- Round Average score stat to 2 decimal places.
- Updated logger format.
- Added additional log info.
- Code cleanups.
****

# v1.2.0.3 - Improvements
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
**Fixes:**
- Removed duplicate entries from List.

**Inside the Code:**
- Rewritten the Code, making the functions outside of the Main script.
- Added Logger function, with Current Time.
****

# v1.0.0.0 - First Version
**Features:**
- Export User Anime/Manga list to JSON file.
- Export User Anime/Manga list to [MAL](https://myanimelist.net/) Xml export file (Can be imported to [MyAnimeList](https://myanimelist.net/import.php)).
- Graphical User Interface, for easy use.