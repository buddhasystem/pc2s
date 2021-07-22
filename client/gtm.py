#!/usr/bin/env python3.5
#
# The script to manage Global Tag Maps with the pc2s system
#
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

user		= os.environ['USER']

server = 'http://localhost:8000/'
verb = 0

parser = argparse.ArgumentParser()

parser.add_argument("-S", "--server",	type=str,
                    help="server URL: defaults to http://localhost:8000/",
                    default=server)

parser.add_argument("-c", "--create", action='store_true',	help="Create a Global Tag")
parser.add_argument("-d", "--delete", action='store_true',	help="Delete a Global Tag")

parser.add_argument("-g", "--global_tag",   type=str,	help="Global Tag Name",	    default='')
parser.add_argument("-t", "--tag",          type=str,	help="Tag",                 default='')

parser.add_argument("-v", "--verbosity",type=int,	help="Verbosity level",     default=0)
########################### Parse all arguments #########################
args = parser.parse_args()

server	= args.server

create  = args.create
delete  = args.delete

gt      = args.global_tag
tag     = args.tag

verb    = args.verbosity

### pc2s interface defined here
API  = serverAPI(server=server, verb=verb)
###########################################

if(create):
    if(gt is None or tag is None):
        print('Please supply valid names for the global tag and the tag')
        exit(-1)
    else:
        resp = API.post2server('cdb', 'gtmcreate', {'globaltag':gt, 'tag':tag})
        print(resp)
        exit(0)

if(delete):
    if(gt is None or tag is None):
        print('Please supply valid names for the global tag and the tag')
        exit(-1)
    else:
        resp = API.post2server('cdb', 'gtmdelete', {'globaltag':gt, 'tag':tag})
        print(resp)
        exit(0)

exit(0)


