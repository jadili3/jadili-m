from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
from account.forms import UserForm
from registration.form import RegisterForm
from django.db import transaction
from account.models import *
from django.contrib import messages
from django.utils.translation import gettext as _




@login_required()
def update_user(request):
    response_data = {'status' : 'failed', 'message' : 'unknown deletion error'}
    if request.is_ajax():
        if request.method == 'POST':
            form = UserForm(instance=request.user, data=request.POST)
            if form.is_valid():
                form.instance.username = form.instance.email
                form.save()
                response_data = {'status' : 'success', 'message' : 'updated user'}
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


                               
