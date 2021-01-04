import json
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from registration.form import RegisterForm
# from .tokens import account_activation_token



def register_modal(request):
    form = RegisterForm()
    return render(request, 'register/modal.html',{
        'form': form,
    })

def redirectedregister(request):
    form = RegisterForm()
    return render(request, 'register/register.html'
    ,{
    'form': form,  
     'local_css_urls': ["css3/easy-responsive-tabs.css",
                            "css3/material-kit.min1036.css",
                            "css3/demo.css",
                            "css3/vertical-nav.css"],
        'local_js_urls': [ "core/jquery.min.js",
                           "core/popper.min.js",
                           "core/bootstrap-material-design.min.js",
                           "js3/vertical-nav.js",
                           "js3/material-kit.min1036.js",
                           "js3/demo.js",
                           "js3/buttons.js",
                           "js3/modernizr.js",                         
                           "js3/bootstrap.min.js",                           
                           "js3/plugins/moment.min.js ",
                           "js3/plugins/bootstrap-datetimepicker.js",
                           "js3/plugins/jquery.flexisel.js",
                           "js3/plugins/jquery.sharrre.js",
                           "js3/plugins/nouislider.min.js",
                           "js3/plugins/bootstrap-selectpicker.js",
                           "js3/plugins/bootstrap-tagsinput.js",
                           "js3/plugins/jasny-bootstrap.min.js"]
      
    })

def register(request):
    response_data = {}
    if request.is_ajax():
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            # Validate the form: the captcha field will automatically
            # check the input
            if form.is_valid():
                response_data = create_user(form)  # Create our store
            else:
                response_data = {'status' : 'failed', 'message' : json.dumps(form.errors)}
    else:
        response_data = {'status' : 'failure', 'message' : 'Not acceptable request made.' }
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def create_user(form):
    # Create the user in our database
    email = form['email'].value().lower()
    try:
        user = User.objects.create_user(
            email,  # Username
            email,  # Email
            form['password'].value(),
        )
        user.first_name = form['first_name'].value()
        user.last_name = form['last_name'].value()
        # user.is_active = False  # Need email verification to change status.
        user.save()
    except Exception as e:
        return {
            'status' : 'failure',
            'message' : 'An unknown error occured, failed registering user.'
    }

    # Return success status
    return {
        'status' : 'success',
        'message' : 'user registered'
    }
