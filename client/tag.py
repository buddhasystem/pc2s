#!/usr/bin/env python3
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
parser.add_argument("-r", "--rename", action='store_true',	help="Rename a Tag")
parser.add_argument("-U", "--usage",  action='store_true',	help="Useful tips")
parser.add_argument("-m", "--modify", action='store_true',	help="Modify the timestamp")

parser.add_argument("-n", "--name",   type=str,	            help="Tag Name",    default='')
parser.add_argument("-N", "--newname",type=str,	            help="New Tag Name (for renaming)", default='')
parser.add_argument("-u", "--until",  type=str,	            help="Valid until", default='')

parser.add_argument("-v", "--verbosity",type=int,	help="Verbosity level",     default=0)
########################### Parse all arguments #########################
args = parser.parse_args()

server	= args.server

create  = args.create
delete  = args.delete
rename  = args.rename
modify  = args.modify
usage   = args.usage

name    = args.name
newname = args.newname
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

if(modify):
    if(until is None or until=='' or name is None or name==''):
        print('Please supply a valid name and the end time of the tag validity for this operation')
        exit(-1)
    else:
        resp = API.post2server('cdb', 'taguntil', {'name':name, 'until':until})
        print(resp)
        exit(0)

if(delete):
    resp = API.post2server('cdb', 'tagdelete', {'name':name})
    print(resp)
    exit(0)

if(rename):
    if(newname is None or newname==''):
        print('Please supply a valid new name for the rename operation')
        exit(-1)
    else:
        resp = API.post2server('cdb', 'tagrename', {'name':name, 'newname':newname})
        print(resp)
        exit(0)

resp=API.simple_get('cdb', 'tag', {'name':name})
print(resp)

exit(0)


