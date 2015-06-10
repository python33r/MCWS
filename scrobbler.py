# -*- coding: utf-8 -*-

import mcws
import pylast
import time
from configparser import ConfigParser

config = ConfigParser()
config.read("mcws.config")

service = mcws.Service(config["server"]["address"])

lastfm = pylast.LastFMNetwork(
  api_key=config["lastfm"]["api_key"],
  api_secret=config["lastfm"]["api_secret"],
  username=config["lastfm"]["username"],
  password_hash=pylast.md5(config["lastfm"]["password"]))

previous = None
while True:
    track = service.get_now_playing()
    if track:
        this = (track["title"], track["artist"], track["album"])
        if this != previous:
            print("{0} [{1} - {2}]".format(*this))
            elapsed = time.strptime(track["elapsed"], "%M:%S")
            elapsed_seconds = 60*elapsed.tm_min + elapsed.tm_sec
            start = int(time.time()) - elapsed_seconds
            lastfm.scrobble(
              artist=track["artist"],
              album=track["album"],
              title=track["title"],
              timestamp=start)
            previous = this
    time.sleep(30)
