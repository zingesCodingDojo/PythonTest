from __future__ import unicode_literals
from django.db import models
from time import strftime
from ..LoginRegistration.models import User


class WishlistManager(models.Manager):
    def validation(self, postData, user_id):

        errors = []
        if len(postData["item"]) < 3:
            errors.append("Item/Product must be 3 at least 3 characters long.")

        response_to_views = {}
        if len(errors):
            response_to_views["status"] = False
            response_to_views["errors"] = errors
        else:
            response_to_views["status"] = True
            new_trip = self.create(item=postData["item"], user=User.objects.get(id=user_id))
            response_to_views["new_trip"] = new_trip
        return response_to_views


class Wishlist(models.Model):
    item = models.CharField(max_length=30)
    user = models.ForeignKey(User, related_name="user_trip", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishlistManager()


class MultiUserWishListManager(models.Manager):
    def add_user(self, newuser, wishlist_id):
        return self.create(liked_user=User.objects.get(id=newuser), item=Wishlist.objects.get(id=wishlist_id))


class MultiUserWishList(models.Model):
    liked_user = models.ForeignKey(User, related_name="Newpees", on_delete=models.CASCADE)
    item = models.ForeignKey(Wishlist, related_name="wishlist_item", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MultiUserWishListManager()