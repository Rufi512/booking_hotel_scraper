from django.shortcuts import render


def hotel(request):
    return render(request, 'index.html')

def rooms(request, hotel_id):
    context_dict = {"hotel":hotel_id}
    return render(request, 'rooms.html', context_dict)
