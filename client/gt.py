#!/usr/bin/env python3.5
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

parser.add_argument("-t", "--test",	action='store_true',	help="do not contact the server - testing the client")

parser.add_argument("-S", "--server",	type=str,
                    help="server URL: defaults to http://localhost:8000/",
                    default=server)

parser.add_argument("-n", "--name",     type=str,	help="Global Tag Name",	    default='')
parser.add_argument("-s", "--status",   type=str,	help="Status to be set",    default='')
parser.add_argument("-v", "--verbosity",type=int,	help="Verbosity level",     default=0)
########################### Parse all arguments #########################
args = parser.parse_args()

server	= args.server
tst	    = args.test # for debugging only

name    = args.name
status  = args.status
verb    = args.verbosity

### pc2s interface defined here
API  = serverAPI(server=server, verb=verb)
d = {}
d['name']   = name
d['status'] = status

if(status==''):
    resp=API.simple_get('cdb', 'gtstatus', {'key':'name', 'value':name})
    print(resp)
    exit(0)
resp = API.post2server('cdb', 'gtstatus', d)
print(resp)

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

