###########################################################################
# This is a dictionary which maps mneumonic keys to URLs of the pc2s       #
# server. It thus allows for more flexibility when changing URLs and also #
# serves as a reference to the server API.                                #
###########################################################################
from comms		import data2post, rdec, communicate

from django.utils.http import urlencode

###########################################################################
class serverAPI(dict):
    def __init__(self, server='http://localhost:8000/', logger=None, verb=0):
        
        self.server	= server
        self.logger	= logger
        self.verb	= verb

        ### CDB
        self['cdb']	= {
            # Global Tag
            'globaltag':        server+'cdb/globaltag',
            'gtlist':           server+'cdb/globaltag/list',
            'gttaglist':        server+'cdb/globaltag/taglist',
            'gtcreate':         server+'cdb/globaltag/create',
            'gtdelete':	        server+'cdb/globaltag/delete',
            # Global Tag Map
            'gtm':              server+'cdb/gtm',
            'gtmcreate':        server+'cdb/gtm/create',
            'gtmdelete':        server+'cdb/gtm/delete',
            # Tag
            'tag':              server+'cdb/tag',
            'tagcreate':        server+'cdb/tag/create',
            'tagdelete':        server+'cdb/tag/delete',
            # Payload
            'payload':          server+'cdb/payload',
            'payloadcreate':    server+'cdb/payload/create',
            'payloaddelete':    server+'cdb/payload/delete',
        }


    def setLogger(self, logger):
        self.logger=logger

    def setVerbosity(self, verb):
        self.verb=verb

        
    ############# GENERAL POST & GET
    def post2server(self, view, url, stuff):
        # print('************', view, url, stuff, self[view][url])
        return rdec(communicate(self[view][url], data=data2post(stuff).utf8(), logger=self.logger, verb=self.verb))
    
    def get2server(self, view, url, stuff):
        if(self.verb>0): print(self[view][url] % stuff)
        resp = communicate(self[view][url] % stuff, logger=self.logger)
        return rdec(resp)

    def simple_get(self, view, url, stuff=None):
        if(stuff is None):
            theURL=self[view][url]
        else:
#            query=[]
#            for k in stuff.keys(): query.append(k+'='+stuff[k])
#            query_string="&".join(query)
#            theURL=self[view][url]+'?'+query_string
            theURL=self[view][url]+'?'+urlencode(stuff)

        if(self.verb>0): print(theURL)
        resp = communicate(theURL, logger=self.logger)
        return rdec(resp)


