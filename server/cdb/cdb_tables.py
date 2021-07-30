import	django_tables2	as tables

from django.utils.safestring    import mark_safe
from django.utils.html          import format_html

from django.urls                import reverse
from django.conf                import settings

from django.db.models	        import Case, When

from .models		            import *

import operator

#####
#########################################################
############## Links formatters #########################
#########################################################
def makelink(what, key, value):
    return mark_safe('<a href="http://%s%s?%s=%s">%s</a>'
                     % (settings.domain, reverse(what), key, value, value))


###
class GlobalTagTable(tables.Table):
    def render_name(self, value):
        return makelink('globaltagdetail', 'name', value)

    class Meta:
        model=GlobalTag

###
class TagTable(tables.Table):
    def render_name(self, value):
        return makelink('tagdetail', 'name', value)

    class Meta:
        model=Tag

###
class PayloadTable(tables.Table):
#    def render_name(self, value):
#        return makelink('globaltagdetail', 'name', value)

    class Meta:
        model=Payload
