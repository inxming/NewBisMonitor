# -*- coding: utf-8 -*-
'''读取配置文件'''

import os
from config import config_file
from ConfigParser import ConfigParser

def readconfigfile():
    if os.path.isfile(config_file):
        rf = ConfigParser()
        rf.read(config_file)
        secs = rf.sections()
        return secs
    else:
        print 'Configuration file does not exist.'