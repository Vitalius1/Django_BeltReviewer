from __future__ import unicode_literals

from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+.[^@\s]+$")
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_and_register(self, postData):
        errors = {}
        
        # First Name Validation
        if not len(postData['first_name']):
            errors['first_name'] = "First name field can not be empty."
        elif  not re.match(NAME_REGEX, postData['first_name']):
            errors['first_name'] = "Invalid first name! Please input only letter characters."
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name too short."
        
        # Last name Validation
        if not len(postData['last_name']):
            errors['last_name'] = "Last name field can not be empty."
        elif  not re.match(NAME_REGEX, postData['last_name']):
            errors['last_name'] = "Invalid last name! Please input only letter characters."
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name too short."
        
        # Email Validation
        if not len(postData['email']):
            errors['email'] = "Email field can not be empty."
        elif not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Invalid email! Please input the right format of an email like: user@mail.com"
        elif self.filter(email = postData['email']):
            errors['email'] = "Error! Email already in use."
        
        # Password Validation
        if not len(postData['password']):
            errors['password'] = "Password field can not be empty."
        elif len(postData['password']) < 8:
            errors['password'] = "Password too short. Input at least 8 characters"
        elif postData['password'] != postData['confirm_pass']:
            errors['confirm_pass'] = "Password not confirmed. Please pay more attention"
       
        # Return of the validation results for register method
        if len(errors):
            return (False, errors)
        else:
            password = postData['password'].encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed)
            return (True, postData['first_name'])

    def validate_and_login(self, postData):
        errors_login = {}
        # Email Validation when Login
        if not len(postData['email']):
            errors_login['login_email_error'] = "Please provide an email."
        else:
            if not self.filter(email = postData['email']):
                errors_login['login_error'] = "Email or password wrong."
        
        if not len(errors_login):
            user = self.filter(email = postData['email'])
        # # Password Validation when Login
            if not len(postData['password']):
                errors_login['login_password_error'] = "Please provide password."
            else:
                password = postData['password'].encode()
                hashed = self.filter(email = postData['email'])[0].password.encode()
                if not bcrypt.checkpw(password, hashed):
                    errors_login['login_error'] = "Email or password wrong."

        
        # Return of the validation results for login method
        if len(errors_login):
            return (False, errors_login)
        else:
            return (True, self.filter(email = postData['email']))





class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()
# Create your models here.
