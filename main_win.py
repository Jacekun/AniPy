# imports
print("Import packages..")
import os
import pygubu
import importlib
import sys
import pygubu.builder.tkstdwidgets
import pygubu.builder.ttkstdwidgets

print("Import scripts from same folder")
fMain = importlib.import_module("func")
fReq = importlib.import_module("anilist_request")

print("Define Global Vars..")
# Global Vars
# App Properties
appVersion = '1.0'
appBuild = '001'

# GUI related
PROJECT_PATH = os.path.dirname(sys.executable) #os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "files\\main_win.ui")

# Variables
# inputUser = ""

print("Start App from Class: 'Main'.")
# Start App
class Main:
  # GUI
  def __init__(self, master=None):
    # build ui
    self.builder = builder = pygubu.Builder()
    builder.add_resource_path(PROJECT_PATH)
    builder.add_from_file(PROJECT_UI)
    self.mainwindow = builder.get_object('gTopLevel')
    builder.connect_callbacks(self)

  def run(self):
    self.mainwindow.mainloop()

  # events
  def buttonExport_callback(self):
    # Get object IDs
    buttonExport = self.builder.get_object('gButtonExport')
    labelStatus = self.builder.get_object('gLabelStatus')

    # Disable button
    buttonExport["state"] = "disabled"
    labelStatus.config(text = "Starting export..")

    # Get User ID, from Username
    labelStatus["text"] = "Getting user ID.."
    username = fMain.validateStr(self.builder.tkvariables['inputUser'].get())
    # Exit if username is null
    if (username is not None):
      # Get User ID, by POST-ing a request to Anilist
      userID = fReq.anilist_getUserID(username)
      if (userID > 0):
        labelStatus["text"] = "User ID received!"
        print("Successfully received the user ID!")

        # Request anime list
        labelStatus["text"] = fMain.logString("Requesting anime list..")

        # Output file names
        outputAnime = os.path.join(PROJECT_PATH, "anime.json")
        xmlAnime = os.path.join(PROJECT_PATH, "anime.xml")
        # Check if not existing
        if not (os.path.exists(outputAnime)):
          # Get JSON object
          jsonAnime = fReq.anilist_userlist(userID, "ANIME")
          labelStatus["text"] = fMain.logString("Checking anime list..")

          # Check if not null
          if jsonAnime is not None:
            listAnime = jsonAnime["data"]["MediaListCollection"]["lists"]
            labelStatus["text"] = fMain.logString("User Anime list received!")

            # Create vars
            # Count Manga entries
            cTotal = 0
            cWatch = 0
            cComplete = 0
            cHold = 0
            cDrop = 0
            cPtw = 0

            # Start generating JSON and XML..
            labelStatus["text"] = fMain.logString("Start generating Anime JSON/XML file..")

            # Write to json file
            fMain.write_append(outputAnime, '[\n')

            # Iterate over the MediaCollection List
            for anime in listAnime:
              animeInfo = anime["entries"]
              # Iterate over the anime information, inside the entries
              for entry in animeInfo:
                # Write to json file
                jsontoAdd = fMain.entry_json(entry, 'anime')
                fMain.write_append(outputAnime, jsontoAdd)

                # Write to MAL Xml File
                malID = fMain.validateInt(entry["media"]["idMal"])
                if malID != '0':
                  # Get XML strings
                  xmltoWrite = fMain.entry_animexml(malID, entry)
                  # Write to xml file
                  fMain.write_append(xmlAnime, xmltoWrite)
                
                  # Add count
                  malstatus = fMain.validateStr(entry["status"])
                  if (malstatus == "COMPLETED"):
                    cComplete = cComplete + 1
                  elif (malstatus == "PAUSED"):
                    cHold = cHold + 1
                  elif (malstatus == "CURRENT"):
                    cWatch = cWatch + 1
                  elif (malstatus == "DROPPED"):
                    cDrop = cDrop + 1
                  elif (malstatus == "PLANNING"):
                    cPtw = cPtw + 1

            # Delete last comma ',', in json file
            labelStatus["text"] = "Finalizing Anime JSON file.."
            print("Remove last comma from Anime JSON file..")
            fMain.write_remove(outputAnime, 3)

            # Write ']' at the end, to json file
            print("Write last ']' to Anime JSON file..")
            fMain.write_append(outputAnime, '\n]')
            print("Done with Anime JSON file..")
            
            # Write to MAL xml file
            labelStatus["text"] = "Finalizing Anime XML file.."
            print("Add closing tag..")
            fMain.write_append(xmlAnime, '</myanimelist>')

            # Total counts
            cTotal = cWatch + cComplete + cHold + cDrop + cPtw
            print("Prepend 'myinfo' to Anime XML file..")
            malprepend = '<?xml version="1.0" encoding="UTF-8" ?>\n<myanimelist>\n'
            malprepend += '\t<myinfo>\n'
            malprepend += '\t\t' + fMain.toMalval('', 'user_id') + '\n'
            malprepend += '\t\t' + fMain.toMalval(username, 'user_name') + '\n'
            malprepend += '\t\t' + fMain.toMalval('1', 'user_export_type') + '\n'
            malprepend += '\t\t' + fMain.toMalval(str(cTotal), 'user_total_anime') + '\n'
            malprepend += '\t\t' + fMain.toMalval(str(cWatch), 'user_total_watching') + '\n'
            malprepend += '\t\t' + fMain.toMalval(str(cComplete), 'user_total_completed') + '\n'
            malprepend += '\t\t' + fMain.toMalval(str(cHold), 'user_total_onhold') + '\n'
            malprepend += '\t\t' + fMain.toMalval(str(cDrop), 'user_total_dropped') + '\n'
            malprepend += '\t\t' + fMain.toMalval(str(cPtw), 'user_total_plantowatch') + '\n'
            malprepend += '\t</myinfo>\n'
            fMain.line_prepender(xmlAnime, malprepend)
            print("Done with Anime XML file..")

            # Done anime
            labelStatus["text"] = "Anime list JSON/XML generated!"
            print("Done! File generated: " + outputAnime)
            print("Done! File generated: " + xmlAnime)

        # Already existing!
        else:
          print(outputAnime + " file already exist!")
        
        # Request manga list
        labelStatus["text"] = fMain.logString("Requesting manga list..")
        # Output file names
        outputManga = os.path.join(PROJECT_PATH, "manga.json")
        xmlManga = os.path.join(PROJECT_PATH, "manga.xml")

        # Check if not existing
        if not (os.path.exists(outputManga)):
          # Get JSON object
          jsonManga = fReq.anilist_userlist(userID, "MANGA")
          labelStatus["text"] = fMain.logString("Checking manga list..")

          # Check if not null
          if jsonManga is not None:
            listManga = jsonManga["data"]["MediaListCollection"]["lists"]
            labelStatus["text"] = fMain.logString("User Manga list received!")

            # Create vars
            # Count Manga entries
            cTotal = 0
            cRead = 0
            cComplete = 0
            cHold = 0
            cDrop = 0
            cPtr = 0

            # Start generating JSON and XML..
            labelStatus["text"] = fMain.logString("Start generating Manga JSON/XML file..")

            # Write to json file
            fMain.write_append(outputManga, '[\n')

            # Iterate over the MediaCollection List
            for manga in listManga:
              mangaInfo = manga["entries"]
              # Iterate over the manga information, inside the entries
              for entry in mangaInfo:
                # Write to json file
                jsontoAdd = fMain.entry_json(entry, 'manga')
                fMain.write_append(outputManga, jsontoAdd)

                # Write to MAL Xml File
                malID = fMain.validateInt(entry["media"]["idMal"])
                if malID != '0':
                  # Get XML strings
                  xmltoWrite = fMain.entry_mangaxml(malID, entry)
                  # Write to xml file
                  fMain.write_append(xmlManga, xmltoWrite)

                  # Add count
                  malstatus = fMain.validateStr(entry["status"])
                  if (malstatus == "COMPLETED"):
                    cComplete = cComplete + 1
                  elif (malstatus == "PAUSED"):
                    cHold = cHold + 1
                  elif (malstatus == "CURRENT"):
                    cRead = cRead + 1
                  elif (malstatus == "DROPPED"):
                    cDrop = cDrop + 1
                  elif (malstatus == "PLANNING"):
                    cPtr = cPtr + 1

          # Delete last comma ',', in json file
          labelStatus["text"] = "Finalizing Manga JSON file.."
          print("Remove last comma from manga JSON file..")
          fMain.write_remove(outputManga, 3)

          # Write ']' at the end, to json file
          print("Write last ']' to manga JSON file..")
          fMain.write_append(outputManga, '\n]')
          print("Done with Manga JSON file..")
          
          # Write to MAL xml file
          labelStatus["text"] = "Finalizing Manga XML file.."
          print("Add closing tag..")
          fMain.write_append(xmlManga, '</myanimelist>')

          # Total counts
          cTotal = cRead + cComplete + cHold + cDrop + cPtr
          print("Prepend 'myinfo' to Manga XML file..")
          malprepend = '<?xml version="1.0" encoding="UTF-8" ?>\n<myanimelist>\n'
          malprepend += '\t<myinfo>\n'
          malprepend += '\t\t' + fMain.toMalval('', 'user_id') + '\n'
          malprepend += '\t\t' + fMain.toMalval(username, 'user_name') + '\n'
          malprepend += '\t\t' + fMain.toMalval('2', 'user_export_type') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cTotal), 'user_total_manga') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cRead), 'user_total_reading') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cComplete), 'user_total_completed') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cHold), 'user_total_onhold') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cDrop), 'user_total_dropped') + '\n'
          malprepend += '\t\t' + fMain.toMalval(str(cPtr), 'user_total_plantoread') + '\n'
          malprepend += '\t</myinfo>\n'
          fMain.line_prepender(xmlManga, malprepend)
          print("Done with Manga XML file..")

          # Done manga
          labelStatus["text"] = "Manga list JSON/XML generated!"
          print("Done! File generated: " + outputManga)
          print("Done! File generated: " + xmlManga)

        else:
          print(outputManga + " file already exist!")

    else:
      print("Username is empty!")

    # Enable button
    buttonExport["state"] = "active"
    labelStatus["text"] = "Done!"

if __name__ == '__main__':
  app = Main()
  app.run()