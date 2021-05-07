import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from mainForm import Ui_mainForm
import importlib
import concurrent.futures
import os

# Import external scripts
fReq = importlib.import_module("func.anilist_request")
fGetAnime = importlib.import_module("func.anilist_getAnime")
fGetManga = importlib.import_module("func.anilist_getManga")
fTrim = importlib.import_module("func.trim_list")
fNotOnTachi = importlib.import_module("func.getNotOnTachi")

# Global Vars
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
entryLog = os.path.join(PROJECT_PATH, "output\\entries.log") # Log entries
AccessTkn = ""
OutputAnime = ""
OutputManga = ""
TachiLib = ""

# Events
def GetUserID(username):
    return fReq.anilist_getUserID(username)

def GetAnimeEntries(list):
    return fGetAnime.getAnimeEntries("", list[0], list[1], PROJECT_PATH, entryLog, False)

def GetMangaEntries(list):
    return fGetManga.getMangaEntries("", list[0], list[1], PROJECT_PATH, entryLog, False)

def TrimResults():
    fTrim.trim_results(PROJECT_PATH, OutputAnime, OutputManga)

def NotOnTachi():
    fNotOnTachi.getNotOnTachi(OutputManga, TachiLib)

def GoSimple(self):
    window.disableButtons() # Prevent button events
    window.setStatus("Starting..")
    # vars
    username = window.getUsername()
    userID = 0

    window.setStatus("Getting user ID..")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threadCall = executor.submit(GetUserID, username)
        userID = threadCall.result()
    
    window.setStatus("Fetching anime list..")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threadCall = executor.submit(GetAnimeEntries, [ userID, username ])
        OutputAnime = threadCall.result()
        print(f'Output anime: {OutputAnime}')
    
    window.setStatus("Fetching manga list..")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threadCall = executor.submit(GetMangaEntries, [ userID, username ])
        OutputManga = threadCall.result()
        print(f'Output manga: {OutputManga}')
    
    window.setStatus("Trimming list..")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threadCall = executor.submit(TrimResults)
    
    window.setStatus("Comparing against Tachiyomi library..")
    TachiLib = window.getTachiFile()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        threadCall = executor.submit(NotOnTachi)
    
    window.setStatus("Done!")
    window.enableButtons()

# Main UI Form
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_mainForm()
        self.ui.setupUi(self)

        # Assign events
        self.ui.btnGoSimple.clicked.connect(GoSimple)

    # Functions
    def setStatus(self, text):
        self.ui.lblStatus.setText(f'Status: {text}')

    def getUsername(self):
        return self.ui.txtUsername.text()
    
    def getTachiFile(self):
        return self.ui.txtTachi.text()
    
    def setToken(self, token):
        self.ui.txtToken.setText(token)
    
    def enableButtons(self):
        self.ui.btnGoSimple.setEnabled(True)
        self.ui.btnGoAdvance.setEnabled(True)
        self.ui.btnFetchToken.setEnabled(True)

    def disableButtons(self):
        self.ui.btnGoSimple.setDisabled(True)
        self.ui.btnGoAdvance.setDisabled(True)
        self.ui.btnFetchToken.setDisabled(True)


# Start
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    print(window.getUsername())

    sys.exit(app.exec_())