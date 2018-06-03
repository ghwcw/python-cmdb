# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-03-27
    Project : cmdb
   FileName : urlsconf.py
Description : 
-------------------------------------------------------------
"""
from assetapp import views
from django.conf.urls import url

app_name='assetapp'

urlpatterns=[
    url(r'^report/$',views.report, name='report'),
    url(r'^dashboard/$',views.dashboard, name='dashboard'),
    url(r'^index/$',views.index, name='index'),
    url(r'^detail/(?P<asset_id>[0-9]+)/$',views.detail, name='detail'),
    url(r'^$', views.dashboard),

]

