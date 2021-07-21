###########################################################################
# This is a dictionary which maps mneumonic keys to URLs of the pc2s       #
# server. It thus allows for more flexibility when changing URLs and also #
# serves as a reference to the server API.                                #
###########################################################################
from comms		import data2post, rdec, communicate

###########################################################################
class serverAPI(dict):
    def __init__(self, server='http://localhost:8000/', logger=None, verb=0):
        
        self.server	= server
        self.logger	= logger
        self.verb	= verb

        ### CDB
        self['cdb']	= {
            'gtstatus':	server+'cdb/gtstatus',
            'gt':	    server+'cdb/gt',
            'gtcreate': server+'cdb/gtcreate',
            'gtdelete':	server+'cdb/gtdelete',
        }

# 'ltype':	server+'jobs/ltype?name=%s'

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

    def simple_get(self, view, url, stuff):
        theURL=self[view][url]+'?'+stuff['key']+'='+stuff['value']
        if(self.verb>0): print(theURL)
        resp = communicate(theURL, logger=self.logger)
        return rdec(resp)


