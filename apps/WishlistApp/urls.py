from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^logout$", views.logout, name="logout"),
    url(r"^new_item$", views.new_items, name="new_item"),
    url(r"^add_new_item$", views.add_new_item, name="add_new_items"),
    url(r"^items/(?P<id>\d+)?", views.item, name="items"),
    url(r"^join/(?P<id>\d+)?", views.join, name="join_items"),
    url(r"^delete/(?P<id>\d+)?", views.delete, name="delete"),
    url(r"^remove/(?P<id>\d+)?", views.remove, name="remove")
]
