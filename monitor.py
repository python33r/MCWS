# -*- coding: utf-8 -*-

import time
import mcws
from configparser import ConfigParser

config = ConfigParser()
config.read("mcws.config")

service = mcws.Service(config["server"]["address"])

if service.is_running:
    last = None
    while True:
        playing = service.get_now_playing()
        details = (playing["artist"], playing["album"], playing["track"])
        if details == last:
            print(".", end="", flush=True)
        else:
            print()
            print(details, end="", flush=True)
            last = details
        time.sleep(30)
else:
    print("Service not running.")
