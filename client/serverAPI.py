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
            'delete':	server+'jobs/delete',
            'purge':	server+'jobs/purge',
            'add':	server+'jobs/add',
            'ltype':	server+'jobs/ltype?name=%s',
            'limit':	server+'jobs/limit',
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

    def simple_get(self, view, url, stuff):
        theURL=self[view][url]+'?'+stuff['key']+'='+stuff['value']
        if(self.verb>0): print(theURL)
        resp = communicate(theURL, logger=self.logger)
        return rdec(resp)
    
    #############
    # Some wrappers for convenience, will keep for now
    
    ############# WORKFLOW
    def deleteAllDagWF(self, what):
        return rdec(communicate(self['workflow']['deleteallURL'] % what, logger=self.logger))

    ############# PILOT
    def registerPilot(self, p):
        pilotData = data2post(p).utf8()
        if(self.verb>1 and self.logger): self.logger.info('Pilot data in UTF-8: %s' % pilotData)
        return rdec(communicate(self['pilot']['registerURL'], pilotData, self.logger)) # will croak if unsuccessful

    def reportPilot(self, p):
        return self.post2server('pilot', 'reportURL', p)

    ############# DATA /deprecated
    #    def registerData(self, d):
    #        return rdec(communicate(self['data']['register'], data2post(d).utf8(), self.logger))

    #    def adjData(self, d):
    #        return rdec(communicate(self['data']['adjdata'], data2post(d).utf8()))

