from django.conf.urls import  include, url
from account.views import profileprod
from account.views import profile
from account.views import setting
from account.views import *


urlpatterns = [
    url(r'^update_password$', setting.update_password),


]