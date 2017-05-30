from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Wishlist, MultiUserWishList
from ..LoginRegistration.models import User


def index(request):

    # If no cookie is saved of the user logging in, please redirect to home page.
    if "logged_user" in request.session:
        pass
    else:
        return redirect(reverse("splashpage:index"))
    secret = None
    for items in MultiUserWishList.objects.all().exclude(liked_user__id=2):
        print(items.liked_user.id)
    context = {
        "current_user": Wishlist.objects.filter(user__pk=request.session["full_user"]),
        "all_users": Wishlist.objects.all(),
        "wanted_item": MultiUserWishList.objects.filter(liked_user__pk=request.session["full_user"]),
        "gimme_name": Wishlist.objects.all().exclude(user_id=request.session["full_user"])
    }

    return render(request, "WishlistApp/index.html", context)


def logout(request):
    if request.method == "POST":
        del request.session["logged_user"]
    return redirect(reverse("splashpage:index"))


def new_items(request):
    if "logged_user" in request.session:
        pass
    else:
        return redirect(reverse("splashpage:index"))
    context = {
        "current_user": request.session["full_user"]
    }

    return render(request, "WishlistApp/NewItem.html", context)


def add_new_item(request):
    if request.method == "POST":

        response_from_models = Wishlist.objects.validation(request.POST, request.session["full_user"])

        if response_from_models["status"]:
            print("Item made")
            new_stuff = response_from_models["new_trip"]
            print(new_stuff)
        else:
            for errors in response_from_models["errors"]:
                messages.error(request, errors)
                return redirect("/wishlist/new_item")

    return redirect(reverse("wishlist:index"))


def item(request, id):
    if "logged_user" not in request.session:
        return redirect(reverse("splashpage:index"))

    context = {
        "current_stuff": Wishlist.objects.get(id=id),
        "multiusers": MultiUserWishList.objects.filter(item=id),
        "logged_user": User.objects.get(id=int(request.session["full_user"]))
    }
    return render(request, "WishlistApp/ItemDeetz.html", context)


def join(request, id):

    gimme_user = MultiUserWishList.objects.add_user(request.session["full_user"], id)

    return redirect(reverse("wishlist:index"))


def delete(request, id):
    Wishlist.objects.get(id=id).delete()
    return redirect(reverse("wishlist:index"))


def remove(request, id):
    MultiUserWishList.objects.get(id=id).delete()
    return redirect(reverse("wishlist:index"))