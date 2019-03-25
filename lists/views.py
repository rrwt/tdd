from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text'))
        return redirect('/lists/the-only-list-in-the-world/')
        
    return render(request, 'home.html')


def view_list(request):
    return render(request, 'list.html', {
        'items': Item.objects.all()
    })
