from django.shortcuts import redirect, render
# from django.http import HttpResponse
from lists.forms import ItemForm
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.

def home_page(request):

    return render(request,'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_) #use custom form save function instead of creating item object manually
            # Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request,'list.html', {'list': list_, "form": form})

    #OLD VERSION without using ItemForm()
    # error = None
    #     try:
    #         item = Item(text=request.POST['text'], list=list_)
    #         item.full_clean()
    #         item.save()
    #         return redirect(list_)
    #     except ValidationError:
    #         error = "You can't have an empty list item"
    # return render(request, 'list.html', {'list':list_, "form": form, 'error': error })

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_) #use custom form save function instead of creating item object manually
        # item = Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
    # OLD IMPLEMENTATION BEFORE using ItemForm
    # try:
    #     item.full_clean() # add full model validation
    #     item.save()
    # except ValidationError:
    #     list_.delete() # delete list if the item is invalid
    #     error = "You can't have an empty list item"
    #     return render(request, 'home.html', {"error": error})
    # return redirect(list_)

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['text'], list=list_)
    return redirect(f'/lists/{list_.id}/')



