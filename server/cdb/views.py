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

from .selector_utils import *

from	django_tables2	import RequestConfig

import markdown

#############################################
statuses    = ['NEW','PUB','INV']
text_width  = '1100px'
main_table_width = '1000px'
main_table_width_max = '1400px'
#####
def index(request, what='test'):
    return render(request, 'index.html')


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
    
    q = request.GET.get('query', '')

    if(q is None or q==''):
        try:
            gts=GlobalTag.objects.all()
        except:
            return HttpResponse("ERR")
    else:
        gts=GlobalTag.objects.filter(name__contains=q)
    
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

#####
@csrf_exempt
def gtrename(request):
    if request.method =='POST':
        post         = request.POST
        name         = post.get('name', None)
        newname      = post.get('newname', None)

        if(name is None or name=='' or newname is None or newname==''):
            return HttpResponse("ERR")

        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
       
        gt.name=newname
        gt.save()

        try:
            GlobalTagMap.objects.filter(globaltag=name).update(globaltag=newname)
        except:
            pass

        try:
            GlobalTag.objects.get(name=name).delete()
        except:
            return HttpResponse("ERR")
        
        return HttpResponse('OK')
    else:
        return HttpResponse('ERR')


#####
@csrf_exempt
def gtstatus(request):
    if request.method =='POST':
        post    = request.POST
        name    = post.get('name',      None)
        status  = post.get('status',    None)

        if(name is None or name==''): return HttpResponse("ERR")

        if(status not in GlobalTag.status_choices()):
            return HttpResponse("ERR")

        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
       
        gt.status=status
        gt.save()
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
def taglist(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else:
        try:
            tags=[str(elem) for elem in list(Tag.objects.values_list('name', flat=True))]
        except:
            return HttpResponse("ERR")

        data = yaml.dump(tags, sort_keys=False)
        return HttpResponse(data)
#####
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
@csrf_exempt
def tagrename(request):
    if request.method =='POST':
        post         = request.POST
        name         = post.get('name', None)
        newname      = post.get('newname', None)

        if(name is None or name=='' or newname is None or newname==''):
            return HttpResponse("ERR")
        
        try:
            tag=Tag.objects.get(name=name)
        except:
            return HttpResponse("ERR")

        tag.name=newname
        tag.save()
        
        try:
            Payload.objects.filter(tag=name).update(tag=newname)
        except:
            pass

        try:
            GlobalTagMap.objects.filter(tag=name).update(tag=newname)
        except:
            pass

        try:
            Tag.objects.get(name=name).delete()
        except:
            return HttpResponse("ERR")

        return HttpResponse('OK')
    else:
        return HttpResponse('ERR')


#####
@csrf_exempt
def taguntil(request):
    if request.method =='POST':
        post         = request.POST
        name         = post.get('name', None)
        until        = post.get('until',None)

        if(name is None or name=='' or until is None or until==''): return HttpResponse("ERR")

        try:
            tag = Tag.objects.get(name=name)
        except:
            return HttpResponse("ERR")

        tag.until=until
        tag.save()
        return HttpResponse('OK')
    else:
        return HttpResponse("ERR")

#####
################################### PAYLOAD ######################
#####
@csrf_exempt
def payload(request):
    if request.method =='POST':
        return HttpResponse("ERR")
    else: # GET
        name  = request.GET.get('name', '')
        gt      = request.GET.get('globaltag', '')
        tag     = request.GET.get('tag', '')
        p_time  = request.GET.get('time', '')

        if(name is not None and name!=''):
            try:
                payload=Payload.objects.get(name=name)
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
            'name':   payload.name,
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
        name      = post.get('name',    None)
        tag         = post.get('tag',       None)
        since       = post.get('since',     None)
        url         = post.get('url',       None)

        # print(name, tag, since, url)

        try:
            found_tag=Tag.objects.get(name=tag)
        except:
            return HttpResponse("ERR")

        p_since = parse_datetime(since)
        if(p_since>=found_tag.until):
            return HttpResponse("ERR")
        
        payload=Payload(name=name, tag=tag, since=since, url=url)
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
        name       = post.get('name', None)

        if(tag is None or tag==''):
            if(name is None or name==''):
                return HttpResponse("ERR")
            else:
                payloads = Payload.objects.filter(name=name)
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
    namepattern = request.GET.get('namepattern', '')
    status      = request.GET.get('status', '')

    search      = 'Search by Partial Name'

    no_name     = namepattern is None or namepattern==''
    no_status   = status is None or status==''

    if(no_name and no_status):
        try:
            gts=GlobalTag.objects.all()
        except:
            return HttpResponse("ERR")
    else:
        gts=None
        if (no_status):
            gts=GlobalTag.objects.filter(name__contains=namepattern)
            search = search_message(namepattern)

        else:
            gts=GlobalTag.objects.filter(status=status)
            if(not no_name):
                search = search_message(namepattern)
                gts=gts.filter(name__contains=namepattern)
            
    # Defer this approach to the selector:
    # selector=gtStatusSelector(request, 'ALL', [('ALL','All'), ('PUB','Published'),])

    gt_table = GlobalTagTable(gts)
    RequestConfig(request, paginate={'per_page': 10}).configure(gt_table)

    items=[('', 'Status Filter: All'),]+GlobalTag.STATUS_CHOICES
    # items = [('', 'Filter'), ('NEW','New'), ('PUB', 'Published'),]
    page_dict = {
        'header':'Global Tags',
        'main_table_width': main_table_width,
        'main_table':       gt_table,
        'search':           search,
        'show_query':       True,
        'show_selector':    True,
        'selector_items':   items,
        'selected':         status,
        'selector_id':      'status',
        }

    return render(request, 'tablepage.html', page_dict)

#####
@csrf_exempt
def tags(request):
    if request.method =='POST':
        return HttpResponse("ERR")

    settings.domain	= request.get_host()
    namepattern     = request.GET.get('namepattern', '')

    search = 'Search'
    if(namepattern is None or namepattern==''):
        try:
            tags=Tag.objects.all()
        except:
            return HttpResponse("ERR")
    else:
        tags=Tag.objects.filter(name__contains=namepattern)
        search=search_message(namepattern)
    
    tag_table = TagTable(tags)
    RequestConfig(request, paginate={'per_page': 10}).configure(tag_table)

    page_dict = {
        'header':           'Tags',
        'main_table_width': main_table_width,
        'main_table':       tag_table,
        'search':           search,
        'show_query':       True,
        }

    return render(request, 'tablepage.html', page_dict)

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
        
        tag_names=[str(elem) for elem in list(GlobalTagMap.objects.filter(globaltag=name).values_list('tag', flat=True))]

        tags=Tag.objects.filter(pk__in=tag_names)
        tagtable = TagTable(tags)
        RequestConfig(request, paginate={'per_page': 10}).configure(tagtable)

        return render(request, 'tablepage.html',
                {
                    'header':mark_safe('Tags for global tag: '+highlight(name)),
                    'main_table_width': main_table_width,
                    'main_table':tagtable
                }
            )

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

        try:
            gtms=GlobalTagMap.objects.filter(tag=name)
            gts=[]
            for gtm in gtms:
                # gts.append(gtm.globaltag)
                gts.append(makelink('globaltagdetail', 'name', gtm.globaltag))
        except:
            pass

        return render(request, 'tablepage.html',
            {
                'header':           mark_safe('Payloads for the tag: '+highlight(name)),
                'main_table_width': main_table_width_max,
                'main_table':       payloadtable,
                'aux_list_header':  mark_safe('Global Tags Referencing tag: '+highlight(name)),
                'aux_list':         gts
                }
            )


#####
@csrf_exempt
def documentation(request, what):

    path = str(settings.DOCUMENTATION)+what # '/documentation.md'

    try:
        file = open(path,mode='r')
    except:
        return render(request, 'textpage.html', {'width': text_width, 'text':'Under construction'})
    
    
    md_docs = file.read()
    file.close()

    md = markdown.Markdown(extensions=['extra'])
    html_docs = md.convert(md_docs) # print(html_docs)

    return render(request, 'textpage.html', {'width': text_width, 'text': html_docs})

#####
@csrf_exempt
def stats(request):
        stat_dict = [
            {'name':'Global Tag',   'count': GlobalTag.objects.all().count()},
            {'name':'Tag',          'count': Tag.objects.all().count()},
            {'name':'Payload',      'count': Payload.objects.all().count()},
            ]
        stattable = StatTable(stat_dict)
        RequestConfig(request, paginate={'per_page': 10}).configure(stattable)

        return render(request, 'tablepage.html',
            {
                'header':           'System Stats',
                'main_table_width': main_table_width,
                'main_table':       stattable,
                }
            )

#####
@csrf_exempt
def test(request):

    items = [('', 'Filter by Status'), ('NEW','New'), ('PUB', 'Published'),]
    return render(request,
                    'test.html',
                    {
                        'selected':     '',
                        'selector_id':  'status',
                        'stuff':        'test',
                        'selector_items':items,
                    }
                )

##### ATTIC
# return render(request, 'cdb.html', {'active': 'cdb', 'message':what})

#print(settings.TIME_ZONE)
#local_tz = pytz.timezone(settings.TIME_ZONE)
