from django.shortcuts import render


def index(request):
    return render(request, 'ts.html', {'active': 'ts'})

def dist(request, t):
    return render(request, 'test_index.html', {'message': 'dist'+str(t)})

