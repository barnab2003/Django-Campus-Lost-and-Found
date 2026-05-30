# items/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Item
from django.db.models import Q  # <--- IMPORT THIS
from .forms import ItemForm, UniversityRegistrationForm
def home(request):
    # Start with all unclaimed items
    items = Item.objects.exclude(status='CLAIMED').order_by('-date_reported')

    # 1. Handle the Search Bar (q)
    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    # 2. Handle the Status Filter (Lost vs Found)
    status_filter = request.GET.get('status')
    if status_filter:
        items = items.filter(status=status_filter)

    return render(request, 'items/home.html', {'items': items})
# --- ADD THIS REGISTRATION VIEW ---
def register(request):
    if request.method == 'POST':
        form = UniversityRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log the user in after signing up
            return redirect('home')
    else:
        form = UniversityRegistrationForm()
    return render(request, 'items/register.html', {'form': form})

# --- PROTECT THIS VIEW ---
@login_required # This forces users to log in before seeing this page
def report_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.reporter = request.user # Now we safely know the user is logged in
            item.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'items/report.html', {'form': form})

# Add this at the bottom of items/views.py

@login_required
def my_dashboard(request):
    # Fetch ONLY the items reported by the currently logged-in user
    my_items = Item.objects.filter(reporter=request.user).order_by('-date_reported')
    return render(request, 'items/my_dashboard.html', {'items': my_items})

@login_required
def mark_as_claimed(request, item_id):
    # Fetch the item, making sure the logged-in user is the one who reported it
    try:
        item = Item.objects.get(id=item_id, reporter=request.user)
        item.status = 'CLAIMED'
        item.save()
    except Item.DoesNotExist:
        # If the item doesn't exist or doesn't belong to them, do nothing
        pass 
        
    return redirect('my_dashboard')

def item_detail(request, item_id):
    # This safely tries to find the item, or shows a 404 page if it doesn't exist
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'items/item_detail.html', {'item': item})