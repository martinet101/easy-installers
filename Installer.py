import time, subprocess
from PySide2 import QtWidgets, QtGui, QtCore
import io, urllib.request
from threading import Thread
from qt_thread_updater import get_updater
import os, sys

running_dir= ""
if getattr(sys, 'frozen', False): # Running as compiled
        running_dir = sys._MEIPASS + "\\" # pylint: disable=no-member
app_codename = "calc"
app_name = "SomePythonThings Calc"
app_link = f"http://www.somepythonthings.tk/versions/{app_codename}.ver"
icon_pic = running_dir+f"{app_codename}.ico"
picture = running_dir+f"{app_codename}.png"
t = None

print(running_dir)

def install():
    root.setMinimumSize(500, 70)
    root.resize(500, 70)
    picAnim.start()
    btnAnim.start()
    cancAnim.start()
    barAnim.start()
    winAnim.start()
    lblAnim.start()
    label.setText(f"Downloading {app_name} installer...")
    for i in range(0, 50):
        time.sleep(0.004)
        picLabel.setPixmap(pixmap.scaled(100-i, 100-i))
        picLabel.resize(100-i, 100-i)
    root.setMaximumSize(500, 70)
    t = Thread(target=download, daemon=True)
    t.start()

def download():
    global msg
    try:
        response = urllib.request.urlopen(app_link)
        response = response.read().decode("utf8")
        version = response.split("///")[0]
        links={'debian': response.split("///")[2].replace('\n', ''), 'win32': response.split("///")[3].replace('\n', ''), 'win64': response.split("///")[4].replace('\n', ''), 'macos':response.split("///")[5].replace('\n', '')}
        try:
            os.remove("\\SomePythonThings\\somepythonthings-{0}-installer.exe".format(app_codename))
        except Exception as e:
            print("Can't remove installer")
        if(os.system("cd %windir%\\..\\Program Files (x86)\\")==0):
            url = (links["win64"])
            print('Win64')
        else:
            url = (links['win32'])
            print('Win32')

        print('Download link is '+url)

        os.chdir("\\")
        try:
            os.chdir("SomePythonThings")
        except FileNotFoundError:
            os.mkdir("SomePythonThings")
            os.chdir("SomePythonThings")

        with urllib.request.urlopen(url) as Response:
            Length = Response.getheader('content-length')
            BlockSize = 10000

            if Length:
                Length = int(Length)
                BlockSize = max(65535, Length // 10000)

            datatowrite = Response.read(0)

            BufferAll = io.BytesIO()
            Size = 0
            while True:
                BufferNow = Response.read(BlockSize)
                datatowrite += BufferNow
                if not BufferNow:
                    break
                BufferAll.write(BufferNow)
                Size += len(BufferNow)
                if Length:
                    percent = int((Size / Length)*100)
                    get_updater().call_in_main(progress.setMaximum, 100)
                    get_updater().call_in_main(progress.setValue, percent)
                    get_updater().call_in_main(label.setText, f"Downloading {app_name} (Version {version}) {percent}% Done")
            with open("/SomePythonThings/somepythonthings-{0}-installer.exe".format(app_codename), 'ab') as f:
                f.write(datatowrite)
        get_updater().call_in_main(progress.setMaximum, 0)
        get_updater().call_in_main(progress.setValue, 0)
        get_updater().call_in_main(label.setText, f"Installing {app_name} (Version {version})...")
        subprocess.run(["%windir%\\..\\SomePythonThings\\somepythonthings-{0}-installer.exe".format(app_codename), "/verysilent"], shell=True)
        get_updater().call_in_main(label.setText, f"{app_name} was installed successfully!")
        get_updater().call_in_main(msg.setIcon, QtWidgets.QMessageBox.Information)
        get_updater().call_in_main(msg.setWindowTitle, "Installation done!")
        get_updater().call_in_main(msg.setText, f"{app_name} was installed successfully to your computer!")
        get_updater().call_in_main(msg.exec_)
        get_updater().call_in_main(sys.exit)
    except Exception as e:
        get_updater().call_in_main(msg.setIcon, QtWidgets.QMessageBox.Critical)
        get_updater().call_in_main(msg.setWindowTitle, "An error occurred")
        get_updater().call_in_main(msg.setText, f"We are unable to download {app_name}. Please check your internet connection and try again later.\n\nError details: {str(e)}")
        get_updater().call_in_main(msg.exec_)
        get_updater().call_in_main(sys.exit)



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
class Window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = Ui_MainWindow()
        ui.setupUi(self)
    
    def closeEvent(self, event):
        if(QtWidgets.QMessageBox.Yes == QtWidgets.QMessageBox.question(root, f"{app_name} Installer", f"Do you really want to abort {app_name} installation?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)):
            event.accept()
        else:
            event.ignore()
        

app = QtWidgets.QApplication([])
root = Window()
root.setWindowIcon(QtGui.QIcon(icon_pic))
root.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint))
root.setWindowTitle(f"{app_name} Installer")
root.setMinimumSize(500, 100)
root.setMaximumSize(500, 100)
root.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
msg = QtWidgets.QMessageBox(root)


picLabel = QtWidgets.QLabel(root)
pixmap = QtGui.QPixmap(picture)
picLabel.setPixmap(pixmap.scaled(100, 100))
picLabel.resize(100, 100)

#labelicon.setStyleSheet(f"""
"""QLabel {{
    border-image: url("{str(picture)}") 0 0 0 0 strech strech;
}}
"""#)
#labelicon.resize(100, 100)
#labelicon.move(0, 0)


label = QtWidgets.QLabel(root)
label.setText(f"Click Install to begin {app_name} installation")
label.resize(310, 100)
label.move(110, 0)

button = QtWidgets.QPushButton(root)
button.setText("Install")
button.clicked.connect(install)
button.resize(70, 100)
button.move(430, 0)

cancel = QtWidgets.QPushButton(root)
cancel.setText("Cancel")
cancel.clicked.connect(root.close)
cancel.resize(70, 0)
cancel.move(430, 0)

progress = QtWidgets.QProgressBar(root)
progress.setFormat("")
progress.setValue(0)
progress.setMinimum(0)
progress.setMaximum(0)
progress.resize(500, 25)
progress.move(0, 100)
progress.setTextVisible(False)

picAnim = QtCore.QPropertyAnimation(picLabel, b"size")
picAnim.setDuration(200)
picAnim.setStartValue(QtCore.QSize(100, 100))
picAnim.setEndValue(QtCore.QSize(50, 50))

picAnim = QtCore.QPropertyAnimation(picLabel, b"size")
picAnim.setDuration(200)
picAnim.setStartValue(QtCore.QSize(100, 100))
picAnim.setEndValue(QtCore.QSize(50, 50))

lblAnim = QtCore.QPropertyAnimation(label, b"geometry")
lblAnim.setDuration(200)
lblAnim.setStartValue(QtCore.QRect(100, 0, 310, 100))
lblAnim.setEndValue(QtCore.QRect(50, 0, 380, 50))

btnAnim = QtCore.QPropertyAnimation(button, b"size")
btnAnim.setDuration(200)
btnAnim.setStartValue(QtCore.QSize(70, 100))
btnAnim.setEndValue(QtCore.QSize(70, 0))

cancAnim = QtCore.QPropertyAnimation(cancel, b"size")
cancAnim.setDuration(200)
cancAnim.setStartValue(QtCore.QSize(70, 0))
cancAnim.setEndValue(QtCore.QSize(70, 50))

barAnim = QtCore.QPropertyAnimation(progress, b"pos")
barAnim.setDuration(200)
barAnim.setStartValue(QtCore.QPoint(0, 100))
barAnim.setEndValue(QtCore.QPoint(0, 50))

winAnim = QtCore.QPropertyAnimation(root, b"size")
winAnim.setDuration(200)
winAnim.setStartValue(QtCore.QSize(500, 100))
winAnim.setEndValue(QtCore.QSize(500, 70))

root.show()
app.exec_()