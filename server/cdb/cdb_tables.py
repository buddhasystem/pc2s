import	django_tables2	as tables

from django.utils.safestring    import mark_safe
from django.utils.html          import format_html

from django.urls                import reverse
from django.conf                import settings

from django.db.models	        import Case, When

from .models		            import *

import operator

#####



class GlobalTagTable(tables.Table):

    def render_name(self, value):

        print(settings.domain, reverse('globaltagdetail'))
        return 'foo'

    
    class Meta:
        model=GlobalTag
        