#! /usr/bin/python3.8

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/Users/xyun/Documents/Online/online_bento4/')
from bento4_web import app as application
application.secret_key = 'anything you wish'