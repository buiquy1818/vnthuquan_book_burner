__author__ = 'quybvs'

import logging
import sys

# config logging here
log = logging.getLogger('')
log.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
log.addHandler(ch)

