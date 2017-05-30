from __future__ import unicode_literals

from django.db import models
import bcrypt


class UserManager(models.Manager):
    def registration_validaiton(self, postData):

        # List will catch user validation errors and display them at the end.
        errors = []

        # Name requires at least one character.
        if len(postData["Name"]) < 1:
            errors.append("Name cannot be empty.")
        elif len(postData["Name"]) < 3:
            errors.append("Name must be 3 or more characters")

        # Username requires at least one character.
        if len(postData["Username"]) < 1:
            errors.append("Username cannot be empty.")
        elif len(postData["Username"]) < 3:
            errors.append("Username must be 3 ore more characters.")

        # Password must be 8 or more characters
        if len(postData["Password"]) < 8:
            errors.append("Password must be 8 or more characters.")

        # Password needs to be confirmed.
        elif postData["PasswordConfirm"] != postData["Password"]:
            errors.append("Passwords do not match.")

        # Usernames cannot be dupes.
        all_users = self.all()
        for items in all_users:
            if postData["Username"] in items.username:
                errors.append("Username is taken. Please select a different Username.")

        # Dictionary to return to the user if validations passed and creating a new user with encrypted password.
        response_to_views = {}

        if len(errors):
            response_to_views["status"] = False
            response_to_views["errors"] = errors
        else:
            response_to_views["status"] = True
            encode_password = postData["Password"].encode()
            hashed_password = bcrypt.hashpw(encode_password, bcrypt.gensalt())
            new_user = self.create(name=postData["Name"], username=postData["Username"], password=hashed_password)
            response_to_views["new_user"] = new_user

        return response_to_views

    def login_validation(self, postData):

        errors = []
        # Username must exist and Username/Password cannot be empty.

        if len(postData["Username"]) < 1:
            errors.append("Username cannot be empty.")

        if len(postData["PasswordLogin"]) < 1:
            errors.append("Password cannot be empty.")

        elif len(postData["PasswordLogin"]) < 8:
            errors.append("Password must be 8 or more characters long.")
        else:

            # Validate Username matches Password in Database.
            user = self.filter(username=postData["Username"])

            if len(user):
                user = self.get(username=postData["Username"])
                encode_password = postData["PasswordLogin"].encode()
                if bcrypt.hashpw(encode_password, salt=user.password.encode()) != user.password:
                    errors.append("Password and Email do not match.")
            else:
                errors.append("Username not found.")

        # Dictionary will be returned.
        response_to_views = {}

        if len(errors):
            response_to_views["status"] = False
            response_to_views["errors"] = errors
        else:
            response_to_views["status"] = True
            response_to_views["user"] = user.name
            response_to_views["full_user"] = user.id

        return response_to_views


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
