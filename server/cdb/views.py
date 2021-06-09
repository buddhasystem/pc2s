from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def index(request):
    return render(request, 'test_index.html', {'message': 'cdb'})

#######################################################
#     return HttpResponse("Future home of the CDB.")

