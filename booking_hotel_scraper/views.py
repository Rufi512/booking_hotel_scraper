from django.shortcuts import render

def hotel(request):
    return render(request, 'index.html')
