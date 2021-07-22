#!/usr/bin/env python3.5
#
# The script to manage Tag pbjects with the pc2s system
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

parser.add_argument("-c", "--create", action='store_true',	help="Create a Tag")
parser.add_argument("-d", "--delete", action='store_true',	help="Delete a Tag")
parser.add_argument("-U", "--usage",  action='store_true',	help="Useful tips")

parser.add_argument("-n", "--name",   type=str,	            help="Tag Name",    default='')
parser.add_argument("-u", "--until",  type=str,	            help="Valid until", default='')

parser.add_argument("-v", "--verbosity",type=int,	help="Verbosity level",     default=0)
########################### Parse all arguments #########################
args = parser.parse_args()

server	= args.server

create  = args.create
delete  = args.delete
usage   = args.usage

name    = args.name
until   = args.until

verb    = args.verbosity

### pc2s interface defined here
API  = serverAPI(server=server, verb=verb)
###########################################
if(usage):
    print("Example of the timestamp format: '2026-07-21 22:50:50+00:00'")
    exit(0)

if(name is None or name==''):
    print('Please supply valid name for the tag')
    exit(-1)

if(create):
    if(until is None or until==''):
        print('Please supply a valid name and the end time of the tag validity')
        exit(-1)
    else:
        resp = API.post2server('cdb', 'tagcreate', {'name':name, 'until':until})
        print(resp)
        exit(0)

if(delete):
    resp = API.post2server('cdb', 'tagdelete', {'name':name})
    print(resp)
    exit(0)


resp=API.simple_get('cdb', 'tag', {'key':'name', 'value':name})
print(resp)

exit(0)


