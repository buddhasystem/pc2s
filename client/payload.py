#!/usr/bin/env python3.5
#
# The script to manage Payload pbjects with the pc2s system
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

parser.add_argument("-c", "--create",   action='store_true',	help="Create a Payload")
parser.add_argument("-d", "--delete",   action='store_true',	help="Delete a Payload")
parser.add_argument("-U", "--usage",    action='store_true',	help="Useful tips")

parser.add_argument("-s", "--sha256",   type=str,	            help="sha256",  default='', nargs='?')
parser.add_argument("-t", "--tag",      type=str,	            help="tag",     default='')
parser.add_argument("-i", "--iov",      type=str,	            help="start of IOV",     default='')
parser.add_argument("-u", "--url",      type=str,	            help="url",     default='')

parser.add_argument("-v", "--verbosity",type=int,	help="Verbosity level",     default=0)
########################### Parse all arguments #########################
args = parser.parse_args()

server	= args.server

create  = args.create
delete  = args.delete
usage   = args.usage

sha256  = args.sha256
tag     = args.tag
since   = args.iov
url     = args.url

if(usage):
    print("Example of the timestamp format: '2026-07-21 22:50:50+00:00'")
    exit(0)

if(sha256 is None or sha256==''):
    print('Automatic calculation of sha256 is not implemented yet, please supply a value')
    exit(-1)

verb    = args.verbosity

### pc2s interface defined here
API  = serverAPI(server=server, verb=verb)
###########################################
if(tag is None or tag==''):
    print('Please supply valid name for the tag')
    exit(-1)

if(create):
    if(since is None or since==''):
        print('Please supply a valid time for the start of validity')
        exit(-1)
    else:
        d={
            'sha256': sha256,
            'tag'   : tag,
            'since' : since,
            'url'   : url
        }
        resp = API.post2server('cdb', 'payloadcreate', d)
        print(resp)
        exit(0)

exit(0)
if(delete):
    resp = API.post2server('cdb', 'tagdelete', {'name':name})
    print(resp)
    exit(0)


resp=API.simple_get('cdb', 'tag', {'key':'name', 'value':name})
print(resp)

exit(0)


