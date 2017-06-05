# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..logreg.models import User
from datetime import datetime
from django.db.models import Q

class TripManager(models.Manager):
    def check_create(self, data, id):
        errors = []
        user = User.objects.get(id=id)
        start = datetime.strptime(data['travel_sdate'], '%Y-%m-%d').date()
        end = datetime.strptime(data['travel_edate'], '%Y-%m-%d').date()
        current = datetime.now().date()
        if len(data['destination']) < 1 or len(data['description']) < 1 or len(data['travel_sdate']) < 1 or len(data['travel_edate']) < 1:
            errors.append(['form', 'All fields are required!'])
        if start < current:
            errors.append(['date', 'Start date must be later than current date.'])
        if end < current:
            errors.append(['date', 'End date cannot be before your current date.'])
        if end < start:
            errors.append(['date', 'End date must be after start date.'])
        if errors:
            return [False, errors]
        else:
            newTrip = trip.objects.create(destination=data['destination'], description=data['description'], trip_creator=user, travel_sdate=data['travel_sdate'],  travel_edate=data['travel_edate'])
            newTrip.save()
            return [True, newTrip]

    def get_trips(self, id):
        return trip.objects.filter(Q(trip_creator=User.objects.get(id=id)) | Q(trip_travelers=User.objects.get(id=id)))

class trip(models.Model):
    destination = models.CharField(max_length=80)
    description = models.TextField()
    travel_sdate = models.DateTimeField()
    travel_edate = models.DateTimeField()
    trip_creator = models.ForeignKey(User, related_name='trip_creator')
    trip_travelers = models.ManyToManyField(User, related_name='trip_travelers')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()
