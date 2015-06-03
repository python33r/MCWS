# -*- coding: utf-8 -*-

import mcws
from configparser import ConfigParser
from pprint import pprint

config = ConfigParser()
config.read("mcws.config")

service = mcws.Service(config["server"]["address"])

if service.is_running:
    pprint(service.get_now_playing())
else:
    print("Service not running.")
