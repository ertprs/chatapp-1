from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ItemForm, ExistingListItemForm
from .models import List, Item

import datetime


def start_a_new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'new_list.html', {'form': form})


def view_list(request, id):
    list_ = List.objects.get(id=id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'your_list.html', {
        'list': list_, "form": form})

def list_view(request):
    lists = List.objects.all()
    return render(request, 'lists.html', {'lists': lists})

def list_detail(request, id):
    list_ = List.objects.get(id=id)
    return redirect(list_)

def delete_item(request, id):
    item = Item.objects.get(id=id)
    item_list = item.list
    list_ = List.objects.get(id=item_list.id)
    item.delete()
    return redirect(list_)

def delete_list(request, id):
    List.objects.get(id=id).delete()
    return redirect('list_view')