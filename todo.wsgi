#! /usr/bin/python3.6

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/todo-project')
from todo import app as application