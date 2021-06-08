from django.shortcuts import render



from django.http import HttpResponse


def index(request):
    return render(request, 'test_index.html', {'message': 'hi'})

def dist(request, t):
    return render(request, 'test_index.html', {'message': 'dist'+str(t)})

