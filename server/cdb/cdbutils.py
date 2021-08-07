from .models import *
from django.utils.dateparse import parse_datetime

###
def tag2dict(name):
    try:
        tag=Tag.objects.get(name=name)
    except:
        return {}

    payloads = Payload.objects.filter(tag=name).order_by('since')
    payload_list=[]

    for p in payloads:
        p_dict={}
        p_dict['sha26'] = p.sha256
        p_dict['since'] = p.since
        p_dict['url']   = p.url
        payload_list.append(p_dict)
        
    result = {'name':tag.name, 'until':tag.until, 'payloads':payload_list}
    return result

###
def find_payload(globaltag, tag, payload_time):
    gtms=GlobalTagMap.objects.filter(globaltag=globaltag, tag=tag)
    if(len(gtms)==0):
        return None

    tag_name=gtms[0].tag
    the_tag=Tag.objects.get(name=tag_name)
    if(payload_time > the_tag.until):
        print('out of range')
        return None

    payloads=Payload.objects.filter(tag=tag_name).order_by('since')
    
    if(len(payloads)==0):
        return None

    start=payloads[0].since

    if(payload_time < start):
        return None

    for p in reversed(payloads):
        if(payload_time>p.since):
            return p

    return None

###
def search_message(name):
    return 'Showing results for "'+name+'". Click here and press <ENTER> to reset search.'
