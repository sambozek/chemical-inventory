from cgitb import text
from django.shortcuts import render, redirect
from inventory_input.models import Item
from inventory_input.tests import ItemModelTest

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/inventory_management/the-only-inv-around/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})