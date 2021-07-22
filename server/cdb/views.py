from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf	import csrf_exempt
import yaml
from yaml.loader import SafeLoader

from .models import *

statuses = ['NEW','PUB','INV']

def index(request, what='test'):
    return render(request, 'cdb.html', {'active': 'cdb', 'message':what})

#####
@csrf_exempt
def gtcreate(request):
    if request.method =='POST':
        post         = request.POST
        yaml_content = post.get('yaml', None)
        name         = post.get('name', None)

        if(name is None and yaml_content is None): return HttpResponse("ERR")

        if(name):
            gt = GlobalTag(name=name)
            gt.save()
            return HttpResponse('OK')

        gt_content = yaml.load(yaml_content, SafeLoader)[0]
        name = list(gt_content.keys())[0]
        attributes = gt_content[name]

        status=attributes['status']
        timestamp=attributes['timestamp']
        if(status and timestamp):
            gt = GlobalTag(name=name, status=status, timestamp=timestamp)
        elif(status):
            gt = GlobalTag(name=name, status=status)
        elif(timestamp):
            gt = GlobalTag(name=name, timestamp=timestamp)
        else:
            gt = GlobalTag(name=name)

        gt.save()
        return HttpResponse('OK')
    else: # GET
        name = request.GET.get('name', '')
        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
        
        to_dump = [{gt.name:{'status':gt.status, 'timestamp':gt.timestamp}},]
        data = yaml.dump(to_dump) #  print(data)
        return HttpResponse(gt.status)

#####
@csrf_exempt
def gtdelete(request):
    if request.method =='POST':
        post         = request.POST
        name         = post.get('name', None)

        if(name is None or name==''): return HttpResponse("ERR")
        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
       
        gt.delete()
        return HttpResponse('OK')
    else:
        return HttpResponse('ERR')

#####
@csrf_exempt
def gtmcreate(request):
    if request.method =='POST':
        post        = request.POST
        globaltag   = post.get('globaltag', None)
        tag         = post.get('tag',       None)

        if(globaltag is None or globaltag=='' or tag is None or tag==''): return HttpResponse("ERR")
        gtm = GlobalTagMap(globaltag=globaltag, tag=tag)
        gtm.save()
        return HttpResponse('OK')
    else:
        return HttpResponse("ERR")

#####
@csrf_exempt
def gtmdelete(request):
    if request.method =='POST':
        post        = request.POST
        globaltag   = post.get('globaltag', None)
        tag         = post.get('tag', None)

        if(globaltag is None or globaltag=='' or tag is None or tag==''): return HttpResponse("ERR")

        gtm = GlobalTagMap.objects.filter(globaltag=globaltag, tag=tag)
        gtm.delete()
        return HttpResponse('OK')
    else:
        return HttpResponse("ERR")

@csrf_exempt
def tag(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else:
        name = request.GET.get('name', '')
        try:
            tag=Tag.objects.get(name=name)
        except:
            return HttpResponse("ERR")

        to_dump = {'name':tag.name, 'until':tag.until}
        data = yaml.dump(to_dump) #  print(data)
        return HttpResponse(data)

#####
@csrf_exempt
def tagcreate(request):
    if request.method =='POST':
        post        = request.POST
        name        = post.get('name',  None)
        until       = post.get('until', None)

        if(name is None or name=='' or until is None or until==''): return HttpResponse("ERR")
        tag = Tag(name=name, until=until)
        tag.save()
        return HttpResponse('OK')
    else:
        return HttpResponse("ERR")

#####
@csrf_exempt
def tagdelete(request):
    if request.method =='POST':
        post         = request.POST
        name         = post.get('name', None)

        if(name is None or name==''): return HttpResponse("ERR")
        try:
            tag=Tag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
       
        tag.delete()
        return HttpResponse('OK')
    else:
        return HttpResponse('ERR')

#####
@csrf_exempt
def payloadcreate(request):
    if request.method =='POST':
        post        = request.POST
        sha256      = post.get('sha256',    None)
        tag         = post.get('tag',       None)
        since       = post.get('since',     None)
        url         = post.get('url',       None)

        print(sha256, tag, since, url)
        payload=Payload(sha256=sha256, tag=tag, since=since, url=url)
        payload.save()

 #       if(name is None or name=='' or until is None or until==''): return HttpResponse("ERR")
 #       tag = Tag(name=name, until=until)
 #       tag.save()
        return HttpResponse('OK')
    else:
        return HttpResponse("ERR")

##### ATTIC
# return render(request, 'cdb.html', {'active': 'cdb', 'message':what})
# return HttpResponse("For debugging only.")

# @csrf_exempt
# def gtstatus(request):
#     if request.method =='POST':
#         post=request.POST
#         name=post.get('name', None)
#         status=post.get('status', None)
#         if status not in statuses: return HttpResponse("ERR")
#         try:
#             gt=GlobalTag.objects.get(name=name)
#         except:
#             return HttpResponse("ERR")

#         gt.status = status
#         gt.save()

#         return HttpResponse(gt.status)
#     else: # GET
#         name = request.GET.get('name', '')
#         try:
#             gt=GlobalTag.objects.get(name=name)
#         except:
#             return HttpResponse("ERR")
        
#         to_dump = [{gt.name:{'status':gt.status, 'timestamp':gt.timestamp}},]
#         data = yaml.dump(to_dump)
#         print(data)
#         return HttpResponse(gt.status)
