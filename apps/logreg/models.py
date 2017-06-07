# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re
USERNAME_REGEX = re.compile(r'^[a-zA-Z.-_]{3,}$')

class UserManager(models.Manager):
    def check_create(self, data):
        errors = []
        if len(data['name']) < 3:
            errors.append(['name', 'Name is invalid. Must contain at least three letters.'])
        if not USERNAME_REGEX.match(data['username']):
            errors.append(['username', 'Username must contain atleast three letters, no spaces and no numbers.'])
        if len(data['password']) < 8:
            errors.append(['password', 'Password must be at least 8 characters.'])
        if data['confirm_pw'] != data['password']:
            errors.append(['password', 'Passwords do not match.'])
        if errors:
            return [False, errors]
        else:
            current_user = User.objects.filter(username=data['username'])
            if current_user:
                errors.append(['current_user', 'Unable to register, please use alternate information.'])
                return [False, errors]
            newUser = User(name=data['name'], username=data['username'], hashed_pass = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()))
            newUser.save()
            return [True, newUser]
    def check_log(self, data):
        errors = []
        current_user = User.objects.filter(username=data['username'])
        if not current_user:
            errors.append(['account', 'username or password incorrect.'])
        elif not bcrypt.checkpw(data['password'].encode(), current_user[0].hashed_pass.encode()):
            errors.append(['account', 'username or password incorrect.'])
        if errors:
            return [False, errors]
        else:
            return [True, current_user[0]]

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    hashed_pass = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
