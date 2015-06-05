# -*- coding: utf-8 -*-

import mcws
from configparser import ConfigParser
from pprint import pprint

config = ConfigParser()
config.read("mcws.config")

service = mcws.Service(config["server"]["address"])

pprint(service.get_now_playing())
