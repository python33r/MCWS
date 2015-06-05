# -*- coding: utf-8 -*-

import mcws, time
from configparser import ConfigParser
from pprint import pprint

config = ConfigParser()
config.read("mcws.config")

service = mcws.Service(config["server"]["address"])

last_sig = None
while True:
    track = service.get_now_playing()
    if track:
        sig = track["artist"]+track["album"]+track["title"]
        if sig != last_sig:
            print()
            pprint(track)
            last_sig = sig
    time.sleep(30)
