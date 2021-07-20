from django.contrib import admin

from .models import *
############
class GlobalTagAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    
admin.site.register(GlobalTag, GlobalTagAdmin)

class PayloadAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

admin.site.register(Payload, PayloadAdmin)    