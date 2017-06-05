# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User

def log_reg(request):
    if request.method == 'POST':
        if request.POST['verify'] == 'register':
            response = User.objects.check_create(request.POST)
            verify = 'registered'
        elif request.POST['verify'] == 'login':
            response = User.objects.check_log(request.POST)
            verify = 'logged in'
        if not response[0]:
            for message in response[1]:
                messages.error(request, message[1])
            return redirect('travelbud:index')
        else:
            request.session['user'] = {
            'id': response[1].id,
            'name': response[1].name
            }
            messages.success(request, 'Successfully ' + verify + '!')
            return redirect('travelbud:travels')
    return redirect('travelbud:index')

def logout(request):
    request.session.clear()
    return redirect('travelbud:index')
