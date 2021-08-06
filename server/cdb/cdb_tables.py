import	django_tables2	as tables

from django.utils.safestring    import mark_safe
from django.utils.html          import format_html

from django.urls                import reverse
from django.conf                import settings

from django.db.models	        import Case, When, Q, Count

from .models		            import *

import operator

#####
#########################################################
###### Link formatters and other helpers ################
#########################################################
def makelink(what, key, value):
    return mark_safe('<a href="http://%s%s?%s=%s">%s</a>'
                     % (settings.domain, reverse(what), key, value, value))

###
def highlight(name):
    return '<span style="color:red;">'+name+'</span>'

####################### Tables ##########################
###
class StatTable(tables.Table):
    name	    = tables.Column(verbose_name='Object', empty_values=())
    count	= tables.Column(verbose_name='#', empty_values=())

#    class Meta:
#        fields =('name', 'count')
###
class GlobalTagTable(tables.Table):
    def render_name(self, value):
        return makelink('globaltagdetail', 'name', value)

    class Meta:
        model=GlobalTag

###
class TagTable(tables.Table):
    global_tags	    = tables.Column(verbose_name='Referenced by Global Tags', empty_values=())
    n_of_payloads	= tables.Column(verbose_name='# of Payloads', empty_values=())

    def render_name(self, value):
        return makelink('tagdetail', 'name', value)

    def render_n_of_payloads(self, record):
        n_of_payloads = Payload.objects.filter(tag=record.name).count()
        return n_of_payloads

    def render_global_tags(self,record):
        gt_url=''
        gtms=GlobalTagMap.objects.filter(tag=record.name)
        gts = []
        for gtm in gtms:
            gt_url=makelink('globaltagdetail', 'name', gtm.globaltag)
            # gts.append(gtm.globaltag)
            gts.append(gt_url)
               
        if(len(gts)==0):
            return '-'
        else:
            return(mark_safe(', '.join(gts)))

    def order_n_of_payloads(self,QuerySet, is_descending):
        return (QuerySet, True)
    
    def order_global_tags(self,QuerySet, is_descending):
        return (QuerySet, True)
    
    class Meta:
        model=Tag

###
class PayloadTable(tables.Table):
#    def render_name(self, value):
#        return makelink('globaltagdetail', 'name', value)

    class Meta:
        model=Payload
        exclude=('tag',)
        sequence=('since', 'url', 'sha256',)
