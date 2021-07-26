from .models import *

def tag2dict(name):
    try:
        tag=Tag.objects.get(name=name)
    except:
        return {}

    payloads = Payload.objects.filter(tag=name)
    payload_list=[]
    for p in payloads:
        p_dict={}
        p_dict['sha26'] = p.sha256
        p_dict['since'] = p.since
        p_dict['url']   = p.url
        payload_list.append(p_dict)
        
    result = {'name':tag.name, 'until':tag.until, 'payloads':payload_list}
    return result
