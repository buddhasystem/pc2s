from django.contrib import admin

from .models import *
############
class GlobalTagAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
admin.site.register(GlobalTag, GlobalTagAdmin)

class GlobalTagMapAdmin(admin.ModelAdmin):
    list_display=['name', 'globaltag','tag']
    empty_value_display = '-empty-'
admin.site.register(GlobalTagMap, GlobalTagMapAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display=['name', 'until']
    empty_value_display = '-empty-'
admin.site.register(Tag, TagAdmin)

class PayloadAdmin(admin.ModelAdmin):
    list_display=['tag','since','url','sha256']
    empty_value_display = '-empty-'
admin.site.register(Payload, PayloadAdmin)
