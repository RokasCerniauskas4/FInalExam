
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm, LoginForm, CreateCategoryForm, NoteForm
from django.contrib import messages
from .models import Category, Note
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request, 'base.html')

# User Views

def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'register.html', {'form': form})


@csrf_protect
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return render(request, 'base.html')


# Category Views


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('show_categories_and_notes')
        return render(request, 'add_category.html', context={'form': form})
    else:
        form = CreateCategoryForm()
    return render(request, 'add_category.html', context={'form': form})


@login_required(login_url='login')
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    notes = Note.objects.filter(category=category)
    notes.delete()
    category.delete()
    return redirect('show_categories_and_notes')

@login_required
def show_categories_and_notes(request, category_id=None):
    search_query = request.GET.get('search')
    categories = Category.objects.filter(user=request.user).all()
    notes = Note.objects.filter(user=request.user, category__isnull=False).all()
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            notes = notes.filter(category=category)
        except Category.DoesNotExist:
            pass
    if search_query:
        notes = notes.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    user_notes = Note.objects.filter(user=request.user, category=None)
    return render(request, 'categories_and_notes.html', {'notes': notes, 'category_id': category_id, 'categories': categories, 'user_notes': user_notes, 'search_query': search_query})


# Note Views

@login_required(login_url='login')
def update_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.category_id = request.POST['category']
        if 'image' in request.FILES:
            note.image = request.FILES['image']
        note.save()
        return redirect('show_categories_and_notes')

    return render(request, 'update_note.html', {'note': note, 'categories':categories})


@login_required(login_url='login')
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('show_categories_and_notes')
    else:
        form = NoteForm(user=request.user)
    return render(request, 'add_note.html', {'form': form})



@login_required(login_url='login')
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('show_categories_and_notes')


