from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf	import csrf_exempt
import yaml

from .models import *

statuses = ['NEW','PUB','INV']

def index(request, what='test'):
    return render(request, 'cdb.html', {'active': 'cdb', 'message':what})
@csrf_exempt
def gtstatus(request):
    if request.method =='POST':
        post=request.POST
        name=post.get('name', None)
        status=post.get('status', None)
        if status not in statuses: return HttpResponse("ERR")
        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")

        gt.status = status
        gt.save()

        return HttpResponse(gt.status)
    else: # GET
        name = request.GET.get('name', '')
        try:
            gt=GlobalTag.objects.get(name=name)
        except:
            return HttpResponse("ERR")
        
        to_dump = [{gt.name:{'status':gt.status, 'timestamp':gt.timestamp}},]
        data = yaml.dump(to_dump)
        print(data)
        return HttpResponse(gt.status)


#    return render(request, 'cdb.html', {'active': 'cdb', 'message':what})
#######################################################
#     return HttpResponse("For debugging only.")

