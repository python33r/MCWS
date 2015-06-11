# -*- coding: utf-8 -*-

import mcws
import pylast
import time
from configparser import ConfigParser

from PyQt4.QtCore import pyqtSlot, Qt, QTimer
from PyQt4.QtGui import QApplication, QWidget
from PyQt4.QtGui import QLineEdit, QTextBrowser, QFormLayout


class Scrobbler(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.configure()
        self.createWidgets()
        self.arrangeWidgets()
        self.setWindowTitle("QtScrobbler")
        self.resize(500, 200)

    def configure(self):
        config = ConfigParser()
        config.read("mcws.config")
        self.service = mcws.Service(config["server"]["address"])
        self.lastfm = pylast.LastFMNetwork(
          api_key=config["lastfm"]["api_key"],
          api_secret=config["lastfm"]["api_secret"],
          username=config["lastfm"]["username"],
          password_hash=pylast.md5(config["lastfm"]["password"]))

    def createWidgets(self):
        self.now = QLineEdit()
        self.now.setStyleSheet("font-weight: bold")
        self.now.setReadOnly(True)
        self.history = QTextBrowser()

    def arrangeWidgets(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Now:", self.now)
        layout.addRow("History:", self.history)
        self.setLayout(layout)

    def startScrobbling(self):
        self.previous = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.scrobble)
        self.timer.start(30000)

    @pyqtSlot()
    def scrobble(self):
        track = self.service.get_now_playing()
        if track:
            this = (track["title"], track["artist"], track["album"])
            if this != self.previous:
                self.now.setText(track["title"])
                self.history.insertHtml("{0} [{1} - {2}]<br>".format(*this))
                elapsed = time.strptime(track["elapsed"], "%M:%S")
                elapsed_seconds = 60*elapsed.tm_min + elapsed.tm_sec
                start = int(time.time()) - elapsed_seconds
                self.lastfm.scrobble(
                  artist=track["artist"],
                  album=track["album"],
                  title=track["title"],
                  timestamp=start)
                self.previous = this


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    scrobbler = Scrobbler()
    scrobbler.startScrobbling()
    scrobbler.show()
    sys.exit(app.exec_())
