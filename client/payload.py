#!/usr/bin/env python3.5
#
# The script to manage Payload pbjects with the pc2s system
#
#########################################################
# TZ-awarewness:					#
# The following is not TZ-aware: datetime.datetime.now()#
# so we are using timzone.now() where needed		#
#########################################################

from django.conf  import settings
from django.utils import timezone

import argparse
import time
import datetime
import os
import string
import random
import hashlib

from yaml.nodes import SequenceNode

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
parser.add_argument("-p", "--populate", type=int,	help="Number of simulated records to create", default=0, nargs='?')

########################### Parse all arguments #########################
args = parser.parse_args()

verb    = args.verbosity
populate=args.populate

server	= args.server

create  = args.create
delete  = args.delete
usage   = args.usage

sha256  = args.sha256
tag     = args.tag
since   = args.iov
url     = args.url

### pc2s interface defined here
API  = serverAPI(server=server, verb=verb)
###########################################
if(tag is None or tag==''):
    print('Please supply valid name for the tag')
    exit(-1)
    
if(populate is not None and populate!=0):
    if(verb>0): print('Will create '+str(populate)+' test records')
    letters = string.ascii_lowercase
    for pop in range(populate):
        random_name =''.join(random.choice(letters) for i in range(10))
        sha256      = hashlib.sha256(random_name.encode()).hexdigest()
        month   = random.randint(1, 12)
        day     = random.randint(1, 30)
        hour    = random.randint(0, 23)
        minute  = random.randint(0, 59)        
        second  = random.randint(0, 59)

        since   = '2026-{:02}-{:02} {:02}:{:02}:{:02}+00:00'.format(month, day, hour, minute, second)

        url = 'https://nginx.sphenix.bnl.gov/cdb/'+random_name+'.root'

        d={'sha256': sha256, 'tag': tag, 'since': since, 'url': url}
        resp = API.post2server('cdb', 'payloadcreate', d)
        if(verb>0): print(resp)
        if(resp=='ERR'): exit(-1)
    exit(0)     

if(usage):
    print("Example of the timestamp format: '2026-07-21 22:50:50+00:00'")
    exit(0)

if(sha256 is None or sha256==''):
    print('Automatic calculation of sha256 is not implemented yet, please supply a value')
    exit(-1)

if(create):
    if(since is None or since==''):
        print('Please supply a valid time for the start of validity')
        exit(-1)
    else:
        d={'sha256': sha256, 'tag': tag, 'since' : since, 'url': url}
        if(verb>1): print(d)         
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


