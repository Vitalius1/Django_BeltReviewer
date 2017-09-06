from django.shortcuts import render, redirect
from django.contrib import messages
from ..log_reg.models import User
from .models import *
from django.core.urlresolvers import reverse


def index(request):
    if not 'user_name' in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('log_reg:index')
    
    reviews = Review.objects.all().order_by('-created_at')[:3]
    books = Book.objects.all()
    context = {
        'reviews': reviews,
        'books':books,
    }
    return render(request, "books/index.html", context)

def logout(request):
    request.session.flush()
    return redirect('log_reg:index')

def add(request):
    if not 'user_name' in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('log_reg:index')
    
    return render(request, "books/add.html")

def create(request):
    if request.method == "POST":
        result = Book.objects.create_book(request.POST)
        print "&&*&*&*&**&&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*"
        if result[0] == False:
            context = {'errors':result[1]}
            return render(request, "books/add.html", context)
        else:
            return redirect(reverse('books:book', kwargs = {"book_id":result[1]}))

def book(request, book_id):
    if not 'user_name' in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('log_reg:index')
    book = Book.objects.get(id = book_id)
    book_reviews = Review.objects.filter(book = book).order_by('-created_at')[:3]
    # print book_reviews, "=========================="
    context = {
        'book':book,
        'reviews':book_reviews,
        'logged_user':User.objects.get(id = request.session['user_id'])
    }
    return render(request, "books/book.html", context)

def add_review(request):
    if request.method == "POST":
        new_review = Review.objects.add_review(request.POST)
        return redirect(reverse('books:book', kwargs = {"book_id":new_review}))

def delete_review(request, review_id):
    
# Create your views here.
