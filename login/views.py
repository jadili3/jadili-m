from django.shortcuts import render
from django.core import serializers
from django.core.mail import send_mail

import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings




def login_modal(request):
    return render(request, 'login/modal.html',{
         'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS
          })

def login_redirect(request):
    return render(request, 'login/login.html',{
          'local_css_urls': ["css/fonts/font-awesome-4.7.0/css/font-awesome.min.css",
                             "css/fonts/iconic/css/material-design-iconic-font.min.css",
                             "css/vendor/animate/animate.css",
	                         "css/vendor/css-hamburgers/hamburgers.min.css",
                             "css/vendor/animsition/css/animsition.min.css",
                             "css/vendor/select2/select2.min.css",
	                         "css/vendor/daterangepicker/daterangepicker.css",
                             "css/vendor/bootstrap/css/bootstrap.min.css",
                             "css/fonts/source-sans-pro/SourceSansPro-Regular.ttf",
                             "css/fonts/source-sans-pro/SourceSansPro-SemiBold.ttf",
                             "css/fonts/source-sans-pro/SourceSansPro-Bold.ttf",
                             "css/util.css",
                             "css/main.css" ],
           'local_js_urls':[ "js2/js/jquery-3.2.1.min.js",
                             "js2/js/animsition.min.js",
                             "js2/js/popper.js",
	                         "js2/js/bootstrap.min.js",
                             "js2/js/select2.min.js",
                             "js2/js/moment.min.js",
	                         "js2/js/daterangepicker.js",
                             "js2/js/countdowntime.js",
                             "js2/js/main.js"],
            })
def trainingbits_redirect(request):
    return render(request, 'login/login2.html',{
         'local_css_urls' : settings.SB_ADMIN_2_CSS_LIBRARY_URLS,
        'local_js_urls' : settings.SB_ADMIN_2_JS_LIBRARY_URLS
          })



def login_authentication(request):
    response_data = {'status' : 'failure', 'message' : 'an unknown error occured'}
    if request.is_ajax():
        if request.method == 'POST':
            user = authenticate(
                username=request.POST.get('username').lower(),
                password=request.POST.get('password')
            )
            
            # Does the user exist for the username and has correct password?
            if user is not None:
                # Is user suspended or active?
                if user.is_active:
                    response_data = {'status' : 'success', 'message' : 'logged on'}
                    login(request, user)
                else:
                    response_data = {'status' : 'failure', 'message' : 'you are suspended'}
            else:
                response_data = {'status' : 'failure', 'message' : 'wrong username or password'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def logout_authentication(request):
    response_data = {'status' : 'success', 'message' : 'you are logged off'}
    if request.is_ajax():
        if request.method == 'POST':
            logout(request)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
