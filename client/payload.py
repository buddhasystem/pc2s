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
parser.add_argument("-f", "--fetch",    action='store_true',	help="Fetch a payload, by hash or Global Tag and time value")
parser.add_argument("-U", "--usage",    action='store_true',	help="Useful tips")

parser.add_argument("-s", "--sha256",       type=str,	help="sha256",  default='', nargs='?')
parser.add_argument("-t", "--tag",          type=str,	help="tag",     default='')
parser.add_argument("-i", "--iov",          type=str,	help="start of IOV ('since')",     default='')
parser.add_argument("-u", "--url",          type=str,	help="url",     default='')

parser.add_argument("-T", "--time",         type=str,	help="time",     default='')
parser.add_argument("-g", "--global_tag",   type=str,   help="Global Tag name",  default='')

parser.add_argument("-v", "--verbosity",    type=int,	help="Verbosity level",     default=0)
parser.add_argument("-p", "--populate",     type=int,	help="For testing only: number of simulated records to create, with random IOVs. Requires a tag name.", default=0, nargs='?')

########################### Parse all arguments #########################
args = parser.parse_args()

verb    = args.verbosity
populate=args.populate

server	= args.server

create  = args.create
delete  = args.delete
fetch   = args.fetch
usage   = args.usage

sha256  = args.sha256
tag     = args.tag
since   = args.iov
url     = args.url

p_time  = args.time
gt      = args.global_tag

### pc2s interface defined here
API  = serverAPI(server=server, verb=verb)
###########################################
if(usage):
    print("Example of the timestamp format: '2026-07-21 22:50:50+00:00'")
    exit(0)



###
# Deletion can be blanket for a tag (i.e. all payloads in a tag are removed)
# or more targeted if the hash is supplied.
if(delete):
    if(sha256 is not None and sha256!=''):
        resp = API.post2server('cdb', 'payloaddelete', {'sha256':sha256})
        if(verb>0): print(resp)
        exit(0)

    if(tag is None or tag==''):
        print('Please supply valid name for the tag for payload deletion')
        exit(-1)

    resp = API.post2server('cdb', 'payloaddelete', {'tag':tag})
    if(verb>0): print(resp)


###
if(fetch):
    if(sha256 is not None and sha256!=''):
        resp=API.simple_get('cdb', 'payload', {'sha256':sha256})
        print(resp)
        exit(0)

    if(gt is None or gt=='' or tag is None or tag==''):
        print('Please supply valid Global Tag and Tag names')
        exit(-1)

    if(p_time is None or p_time==''): p_time=str(timezone.now())
    
    resp=API.simple_get('cdb', 'payload', {'globaltag':gt, 'tag': tag, 'time':p_time})
    print(resp)   
    exit(0)
        

###
if(tag is None or tag==''):
    print('Please supply valid name for the tag')
    exit(-1)

###
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
###
if(create):
    if(sha256 is None or sha256==''):
        print('Automatic calculation of sha256 is not implemented yet, please supply a value')
        exit(-1)
    if(since is None or since==''):
        print('Please supply a valid time for the start of validity')
        exit(-1)

    d={'sha256': sha256, 'tag': tag, 'since' : since, 'url': url}
    if(verb>1): print(d)         
    resp = API.post2server('cdb', 'payloadcreate', d)
    if(verb>0): print(resp)
    exit(0)


exit(0)



