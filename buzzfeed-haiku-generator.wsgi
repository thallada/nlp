import os
import sys
sys.path.append('/var/www/buzzfeed-haiku-generator')

import logging
logging.basicConfig(stream=sys.stderr)

from app import app as application
