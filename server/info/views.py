from django.shortcuts import render


from django.http import HttpResponse


def index(request):
    return render(request, 'index.html', {'message': 'hi'})

#######################################################
#     return HttpResponse("Future home of the CDB.")

