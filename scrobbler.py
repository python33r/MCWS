# -*- coding: utf-8 -*-

import mcws
import pylast
import time
from configparser import ConfigParser
from pprint import pprint

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
        this = track["artist"]+track["album"]+track["title"]
        if this != previous:
            print()
            pprint(track)
            lastfm.scrobble(
              artist=track["artist"],
              album=track["album"],
              title=track["title"],
              timestamp=int(time.time()))
            previous = this
    time.sleep(30)
