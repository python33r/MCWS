# -*- coding: utf-8 -*-

import mcws
from configparser import ConfigParser
from pprint import pprint

config = ConfigParser()
config.read("mcws.config")

server = mcws.Server(config["server"]["address"])
pprint(server.get_now_playing())
