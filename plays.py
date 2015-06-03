# -*- coding: utf-8 -*-

import mcws
from configparser import ConfigParser

config = ConfigParser()
config.read("mcws.config")

server = mcws.Server(config["server"]["address"])
tracks = server.get_played_tracks()

for track in tracks:
    print("{}, {}: plays={}, last at {}".format(
      track["artist"], track["title"], track["plays"], track["last"]))
