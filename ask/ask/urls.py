"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from qa.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^question/(?P<id>\d+)/$', question_details, name='details'), #4 name link to get_absolute_url in Question-model in models.py
    url(r'^$', main), #3
    url(r'^login/$', login),
    url(r'^signup/$', signup),
    url(r'^logout/$', logout),
    url(r'^ask/$', ask_form),
    url(r'^popular/$', test),
    url(r'^new/$', test),
    url(r'^answer_add/$', answer_form), #6!
    url(r'^answer/(?P<id>\d+)/$', answer_details, name='answer_details'), #6!
    url(r'^t/$', t)
]