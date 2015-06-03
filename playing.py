# -*- coding: utf-8 -*-

import mcws
from configparser import ConfigParser
from pprint import pprint

config = ConfigParser()
config.read("mcws.config")

service = mcws.Service(config["server"]["address"])

if service.is_running:
    playing = service.get_now_playing()
    if playing is not None:
        pprint(playing)
else:
    print("Service not running.")
