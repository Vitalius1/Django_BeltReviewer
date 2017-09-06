from __future__ import unicode_literals

from django.db import models
from ..log_reg.models import User

class AuthorManager(models.Manager):
    def create_author(self, data):
        author = self.create(name = data)
        return author

class ReviewManager(models.Manager):
    def add_review(self, postData):

        the_user = User.objects.get(id = postData['user_id'])
        the_book = Book.objects.get(id = postData['book_id'])
        new_review = Review.objects.create(user = the_user, book = the_book, content = postData['review'], rating = postData['rating'])
        return the_book.id


class BookManager(models.Manager):
    def create_book(self, postData):
        errors = {}
        author = ''

        # Checking if author was choosen from existing ones or given a new name
        if not postData['existing_author'] and not postData['new_author']:
            errors['author_error'] = "Please choose an author from already existing ones..."
            errors['author_error2'] = "...or add a new author."
        else:
            if postData['new_author']:
                author = postData['new_author']
            else:
                author = postData['existing_author']
        
        if "author_error" not in errors:  # if no errors so far we either create one or select one
            # Checking if the author already exists get the object if not than create one
            if len(Author.objects.filter(name = author)) < 1:
                the_author = Author.objects.create_author(author)
            else:
                the_author = Author.objects.get(name = author)  # an object of the author instance
        
            print "*****************"
            if not postData['title']:
                errors['title_error'] = "Please give a title."
            else:
                if len(self.filter(title = postData['title'], author = the_author)) > 0:
                    errors['title_error'] = "The book with the title and author you provided already exists."
                else:
                    the_title = postData['title']
                    print the_title, "@@@@@@@@@@@@@@@@@"
        
        if not postData['review']:
            errors['review_error'] = "Please give a review to the book."
        if not postData['rating']:
            errors['rating_error'] = "Please rate the book."

        if not len(errors):
            the_user = User.objects.get(id = postData['user_id'])
            the_book = self.create(title = the_title, author = the_author)
            the_review = Review.objects.create(user = the_user, book = the_book, content = postData['review'], rating = postData['rating'])
            # print the_review.user.first_name
            # print the_review.book.title
            # print the_review.book.avg_rating
        else:
            return (False, errors)
        
        
        
        return (True, the_book.id)
        




class Author(models.Model):
    name = models.CharField(max_length = 128)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = AuthorManager()
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length = 128)
    avg_rating = models.FloatField(default = 0.0)
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name = "books")
    reviews = models.ManyToManyField(User, through = "Review")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = BookManager()
    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "reviews")
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = "books")
    content = models.TextField(max_length = 500)
    rating = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = ReviewManager()


# Create your models here.
