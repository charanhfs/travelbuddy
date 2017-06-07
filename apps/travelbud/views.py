# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import trip
from django.contrib import messages
from ..logreg.models import User

# Create your views here.
def index(request):
    return render(request,'travelbud/index.html')

def travels(request):
    if 'user' in request.session:
        context = {
        'user_trips': trip.objects.get_trips(request.session['user']['id']),
        'other_trips': trip.objects.exclude(id__in=trip.objects.get_trips(request.session['user']['id']))
        }
        print context['other_trips']
        return render(request,'travelbud/dashboard.html', context)
    else:
        return redirect('travelbud:index')


def add_travel_plan(request):
    return render(request,'travelbud/add.html')

def newTravelPlan(request):
    if request.method == 'POST':
        response = trip.objects.check_create(request.POST, request.session['user']['id'])
        if not response[0]:
            for message in response[1]:
                messages.error(request, message[1])
            return redirect('travelbud:add')
        else:
            return redirect('travelbud:travels')
    return redirect('travelbud:add')

def destination(request, id):
    context = {
    'trip': trip.objects.get(id=id),
    'userObj': User.objects.filter(trip_travelers__id=id)
    }
    return render(request, 'travelbud/destination.html', context)

def join(request, id):
    user = User.objects.get(id=request.session['user']['id'])
    trips = trip.objects.get(id=id)
    trips.trip_travelers.add(user)
    trips.save()
    return redirect('travelbud:travels')
