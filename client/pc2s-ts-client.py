#!/usr/bin/env python3


#################################################################
# ATTENTION - this is a placeholder, not a working piece of code.
#################################################################

#########################################################
# TZ-awarewness:					#
# The following is not TZ-aware: datetime.datetime.now()#
# so we are using timzone.now() where needed		#
#########################################################

from django.conf import settings
from django.utils import timezone

import argparse
import time
import datetime
import os

from serverAPI		import serverAPI


#########################################################
settings.configure(USE_TZ = True)

server = 'http://localhost:8000/'
verb = 0

parser = argparse.ArgumentParser()

parser.add_argument("-t", "--test",	action='store_true',	help="do not contact the server - testing the client")

parser.add_argument("-S", "--server",	type=str,
                    help="server URL: defaults to http://localhost:8000/",
                    default=server)

parser.add_argument("-j", "--json_in",	type=str,	help="JSON file with job templates (list)",		default='')

########################### Parse all arguments #########################
args = parser.parse_args()

server	= args.server
tst	= args.test
### pc2s interface defined here
API  = serverAPI(server=server, verb=verb)

###################### GRAND FINALE ####################################
exit(0)

