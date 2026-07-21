import json
from unittest import result
from urllib import request
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Candidate


def index(request):
    candidates = Candidate.objects.all()
    return render(request, 'vote/index.html', {'candidates': candidates})
