from django.shortcuts import render


from django.http import HttpResponse

###
def index(request):
    return render(request, 'index.html', {'message': 'hi'})

###
def ping(request):
    return HttpResponse("OK\n")
