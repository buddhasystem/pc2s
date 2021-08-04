#!/usr/bin/env python3.5
#
# The script to manage Global Tags with the pc2s system
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

from django.utils.http import urlencode

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

parser.add_argument("-c", "--create",       action='store_true',	help="Create a Global Tag")
parser.add_argument("-d", "--delete",       action='store_true',	help="Delete a Global Tag")
parser.add_argument("-l", "--list_gt",      action='store_true',	help="List names of all Global Tags")
parser.add_argument("-t", "--tag_list",     action='store_true',	help="List names of tags in a Global Tag")
parser.add_argument("-n", "--name",         type=str,	            help="Global Tag Name",	    default='')
parser.add_argument("-q", "--query",        type=str, help="Partial Name to narrow down the list of Global Tags",default='')
parser.add_argument("-s", "--status",       type=str, help="Set status: NEW, INV, PUB",    default='')
parser.add_argument("-y", "--yaml_file",    type=str,	            help="YAML definition",     default='', nargs='?')
parser.add_argument("-v", "--verbosity",    type=int,	            help="Verbosity level",     default=0)
########################### Parse all arguments #########################
args = parser.parse_args()

server	= args.server

create  = args.create
delete  = args.delete
list_gt = args.list_gt
tag_list= args.tag_list

name    = args.name
query   = args.query
status  = args.status

y_file  = args.yaml_file

verb    = args.verbosity

### pc2s interface defined here
API  = serverAPI(server=server, verb=verb)
###########################################


if(create):
    if(name is not None and name!=''):
        resp = API.post2server('cdb', 'gtcreate', {'name':name})
        print(resp)
        exit(0)
    

    if(y_file is None or y_file==''):
        print('Please supply a YAML file name or a global tag name')
        exit(-1)
    else:
        try:
            file = open(y_file,mode='r')
        except:
            print('Could not open the Global Tag definition file (YAML):'+y_file)
            exit(-1)
        # read all lines at once
        all_of_it = file.read()
        file.close()
        resp = API.post2server('cdb', 'gtcreate', {'yaml':all_of_it})
        print(resp)
        exit(0)

if(delete):
    if(name is None or name==''):
        print('Please provide a valid global tag name')
        exit(-1)
    
    resp = API.post2server('cdb', 'gtdelete', {'name':name})
    print(resp)
    exit(0)

if(list_gt):
    if(query is not None and query!=''):
        resp=API.simple_get('cdb', 'gtlist', {'query':query})
    else:
        resp=API.simple_get('cdb', 'gtlist')

    print(resp)
    exit(0)

# Print information about a specific tag, so a name is needed:
if(name is None or name==''):
    print('Please provide a valid global tag name')
    exit(-1)

if(tag_list):
    resp=API.simple_get('cdb', 'gttaglist', {'name':name})
    print(resp)
    exit(0)

if(status):
    resp = API.post2server('cdb', 'gtstatus', {'name':name, 'status':status})
    if verb>0: print(resp)
    exit(0)

resp=API.simple_get('cdb', 'globaltag', {'name':name})
print(resp)
exit(0)

