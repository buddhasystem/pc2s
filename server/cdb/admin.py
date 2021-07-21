from django.contrib import admin

from .models import *
############
class GlobalTagAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
admin.site.register(GlobalTag, GlobalTagAdmin)

class GlobalTagMapAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
admin.site.register(GlobalTagMap, GlobalTagMapAdmin)

class TagAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
admin.site.register(Tag, TagAdmin)

class PayloadAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
admin.site.register(Payload, PayloadAdmin)

class IOVAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
admin.site.register(IOV, IOVAdmin) 