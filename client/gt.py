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
parser.add_argument("-n", "--name",         type=str,	            help="Global Tag Name",	    default='')
parser.add_argument("-s", "--status",       type=str,	            help="Status to be set",    default='')
parser.add_argument("-y", "--yaml_file",    type=str,	            help="YAML definition",     default='', nargs='?')
parser.add_argument("-v", "--verbosity",    type=int,	            help="Verbosity level",     default=0)
########################### Parse all arguments #########################
args = parser.parse_args()

server	= args.server

create  = args.create
delete  = args.delete

name    = args.name
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
    resp = API.post2server('cdb', 'gtdelete', {'name':name})
    print(resp)
    exit(0)

exit(0)

# if(status==''):
#     resp=API.simple_get('cdb', 'gt', {'key':'name', 'value':name})
#     print(resp)
#     exit(0)
# resp = API.post2server('cdb', 'gtstatus', d)
# print(resp)

################# JOB TYPES: DUMP AND SET LIMITS   #####################

# if(ltype):
#     if(limit>=0):
#         d = {}
#         d["name"]	= jobtype
#         d["limit"]	= limit
#         resp = API.post2server('job', 'limit', d)
#         if(verb>0): print(resp)
#         exit(0)

        
#     resp = API.get2server('job', 'ltype', jobtype)
#     if(verb>0): print(resp)

#exit(0)
    

########################## UPDATE/ADJUSTMENT ###########################
# Check if an adjustment of an existing job is requested, and send a
# request to the server to do so. Can adjust priority, state.

# if(adj):
#     response = None
#     if(j_uuid==''):			exit(-1) # check if we have the key
#     if(priority==-1 and state==''):	exit(-1) # nothing to adjust

#     if ',' in j_uuid:
#         jobList = j_uuid.split(',')
#     else:
#         jobList.append(j_uuid)
        
#     for j in jobList:
#         a = dict(uuid=j) # create a dict to be serialized and sent to the server
#         if(priority>0):	a['priority']	= str(priority)
#         if(state!=''):	a['state']	= state
#         resp = API.post2server('job', 'adjust', a)
#         if(verb>0): print(resp)

#     exit(0) # done with update/adjust



    # for j in jobList:# Contact the server, register the job(s)
        
    #     if(verb>1): print(j)
        
    #     if(tst): continue # just testing
        
    #     resp = API.post2server('job', 'add', j)
        
    #     if(verb>0): print(resp)
        
    #     time.sleep(delay/1000.0) # delay to prevent a self-inflicted DOS attack



    ###################### GRAND FINALE ####################################
exit(0)

