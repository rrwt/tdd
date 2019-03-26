from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    return render(request, 'list.html', {
        'items': Item.objects.all()
    })


def new_list(request):
    Item.objects.create(text=request.POST['item_text'], list=List.objects.create())
    return redirect('/lists/the-only-list-in-the-world/')
