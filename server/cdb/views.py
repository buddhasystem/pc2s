from django.conf import settings
import pytz
from datetime import datetime
from django.utils.dateparse import parse_datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf	import csrf_exempt
import yaml
from yaml.loader import SafeLoader

from .models import *
from .cdb_tables import *
from .cdbutils import *

from	django_tables2	import RequestConfig

import markdown

statuses = ['NEW','PUB','INV']

def index(request, what='test'):
    return render(request, 'index.html')

#return render(request, 'cdb.html', {'active': 'cdb', 'message':what})


#####
@csrf_exempt
def globaltag(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else: # GET
        name = request.GET.get('name', '')
        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
        
        gtms=GlobalTagMap.objects.filter(globaltag=name)
        tags=[]
        for gtm in gtms:
            tags.append(tag2dict(gtm.tag))

        to_dump = {'name':gt.name, 'status':gt.status, 'tags':tags}
        data = yaml.dump(to_dump, sort_keys=False) #  print(data)
        return HttpResponse(data)


#####
@csrf_exempt
def gttaglist(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else: # GET
        name = request.GET.get('name', '')
        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
        
        gtms=GlobalTagMap.objects.filter(globaltag=name)
        tagnames=[]
        for gtm in gtms:
            tagnames.append(gtm.tag)

        to_dump = {'name':gt.name, 'tags':tagnames}
        data = yaml.dump(to_dump, sort_keys=False) #  print(data)
        return HttpResponse(data)
#####
@csrf_exempt
def gtlist(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    
    try:
        gts=GlobalTag.objects.all()
    except:
        return HttpResponse("ERR")
    
    gt_list=[]
    for gt in gts:
        gt_list.append({'name': gt.name})

    data = yaml.dump(gt_list, sort_keys=False)
    return HttpResponse(data)

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

####################### Global Tag Map #########################
@csrf_exempt
def gtm(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else:
        name = request.GET.get('name', '')
        try:
            gtm=GlobalTagMap.objects.get(name=name)
        except:
            return HttpResponse("ERR")

        to_dump = {'name':gtm.name, 'globaltag':gtm.globaltag, 'tag':gtm.tag}
        data = yaml.dump(to_dump, sort_keys=False) #  print(data)
        return HttpResponse(data)

#####
@csrf_exempt
def gtmcreate(request):
    if request.method =='POST':
        post        = request.POST
        name        = post.get('name',      None)
        globaltag   = post.get('globaltag', None)
        tag         = post.get('tag',       None)

        if(name is None or name=='' or globaltag is None or globaltag=='' or tag is None or tag==''): return HttpResponse("ERR")
        gtm = GlobalTagMap(name=name, globaltag=globaltag, tag=tag)
        gtm.save()
        return HttpResponse('OK')
    else:
        return HttpResponse("ERR")

#####
@csrf_exempt
def gtmdelete(request):
    if request.method =='POST':
        post        = request.POST
        name        = post.get('name', None)

        if(name is None or name==''): return HttpResponse("ERR")

        gtm = GlobalTagMap.objects.get(name=name)
        gtm.delete()
        return HttpResponse('OK')
    else:
        return HttpResponse("ERR")



################################### TAG ##########################
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

        to_dump = tag2dict(name)
        data = yaml.dump(to_dump, sort_keys=False) #  print(data)
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

        payloads = Payload.objects.filter(tag=name)
        try:
            payloads.delete()
        except:
            pass

        tag.delete()
        return HttpResponse('OK')
    else:
        return HttpResponse('ERR')

#####
################################### PAYLOAD ######################
#####
@csrf_exempt
def payload(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else: # GET
        sha256  = request.GET.get('sha256', '')
        gt      = request.GET.get('globaltag', '')
        tag     = request.GET.get('tag', '')
        p_time  = request.GET.get('time', '')

        if(sha256 is not None and sha256!=''):
            try:
                payload=Payload.objects.get(sha256=sha256)
            except:
                return HttpResponse("ERR")
        elif(gt is not None and gt!='' and p_time is not None and p_time!=''):
            try:
                # print(p_time)
                payload=find_payload(gt, tag, parse_datetime(p_time))
            except:
                return HttpResponse("ERR")   
        else:
            return HttpResponse("ERR")

        if(payload is None):
            return HttpResponse("ERR")

        to_dump={
            'sha256':   payload.sha256,
            'tag':      payload.tag,
            'since':    payload.since,
            'url':      payload.url
            }
        data = yaml.dump(to_dump, sort_keys=False) #  print(data)
        return HttpResponse(data)


#####
@csrf_exempt
def payloadcreate(request):
    if request.method =='POST':
        post        = request.POST
        sha256      = post.get('sha256',    None)
        tag         = post.get('tag',       None)
        since       = post.get('since',     None)
        url         = post.get('url',       None)
####### print(sha256, tag, since, url)

        try:
            found_tag=Tag.objects.get(name=tag)
        except:
            return HttpResponse("ERR")

        p_since = parse_datetime(since)
        if(p_since>=found_tag.until):
            return HttpResponse("ERR")
        
        payload=Payload(sha256=sha256, tag=tag, since=since, url=url)
        payload.save()
        return HttpResponse('OK')
    else:
        return HttpResponse("ERR")

#####
@csrf_exempt
def payloaddelete(request):
    if request.method =='POST':
        post         = request.POST
        tag          = post.get('tag', None)
        sha256       = post.get('sha256', None)

        if(tag is None or tag==''):
            if(sha256 is None or sha256==''):
                return HttpResponse("ERR")
            else:
                payloads = Payload.objects.filter(sha256=sha256)
                try:
                    payloads.delete()
                    return HttpResponse('OK')
                except:
                    return HttpResponse('ERR')

        payloads = Payload.objects.filter(tag=tag)
        try:
            payloads.delete()
        except:
            return HttpResponse('ERR')

        return HttpResponse('OK')



###################### MONITOR ###################################
#####
@csrf_exempt
def globaltags(request):
    if request.method =='POST':
        return HttpResponse("ERR")

    settings.domain	= request.get_host()

    try:
        gts=GlobalTag.objects.all()
    except:
        return HttpResponse("ERR")

    gt_table = GlobalTagTable(gts)
    RequestConfig(request, paginate={'per_page': 10}).configure(gt_table)

    return render(request, 'tablepage.html', {'header':'Global Tags', 'width': '400px', 'main_table':gt_table})


#####
@csrf_exempt
def globaltagdetail(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else: # GET
        domain		= request.get_host()
        settings.domain	= domain

        name = request.GET.get('name', '')
        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
        
        gtms=GlobalTagMap.objects.filter(globaltag=name)
        tag_names=[]
        for gtm in gtms:
            tag_names.append(gtm.tag)

        tags=Tag.objects.filter(pk__in=tag_names)
        tagtable = TagTable(tags)
        RequestConfig(request, paginate={'per_page': 10}).configure(tagtable)

        return render(request, 'tablepage.html', {'header':'Tags', 'width': '400px', 'main_table':tagtable})

#####
@csrf_exempt
def tagdetail(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else: # GET
        domain		= request.get_host()
        settings.domain	= domain

        name = request.GET.get('name', '')
        try:
            gt=Tag.objects.get(name=name)
        except:
            return HttpResponse("ERR")

        payloads = Payload.objects.filter(tag=name).order_by('since')
        payloadtable = PayloadTable(payloads)
        RequestConfig(request, paginate={'per_page': 10}).configure(payloadtable)

        return render(request, 'tablepage.html', {'header':'Tags', 'width': '800px', 'main_table':payloadtable})


#####
@csrf_exempt
def documentation(request):
    path = str(settings.DOCUMENTATION)+'/documentation.md'
    try:
        file = open(path,mode='r')
    except:
        return render(request, 'textpage.html', {'header':'Documentation', 'width': '800px', 'text':'Under construction'})
    # read all lines at once

    md_docs = file.read()
    file.close()

    md = markdown.Markdown(extensions=['extra'])
    html_docs = md.convert(md_docs) # print(html_docs)

    return render(request,
                    'textpage.html',
                    {
                        'header':'PC2S - documentation',
                        'width': '1000px',
                        'text':html_docs
                        }
                    )

##### ATTIC
# return render(request, 'cdb.html', {'active': 'cdb', 'message':what})

#print(settings.TIME_ZONE)
#local_tz = pytz.timezone(settings.TIME_ZONE)
