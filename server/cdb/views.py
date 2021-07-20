from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def index(request, what='test'):
    return render(request, 'cdb.html', {'active': 'cdb', 'message':what})

#######################################################
#     return HttpResponse("For debugging only.")

