from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^logout$', views.logout, name = "logout"),
    url(r'^add$', views.add, name = "add"),
    url(r'^create$', views.create, name = "create"),
    url(r'^add_review$', views.add_review, name = "add_review"),
    url(r'^(?P<book_id>\d+)$', views.book, name = "book"),
    url(r'^(?P<review_id>\d+)$', views.delete_review, name = "delete_review"),
]