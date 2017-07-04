#!coding=utf8
#!/usr/bin/env python
'''
Copyright: Copyright (c) 2017
@description:
@author xiaoyun.yang
@date 2017年06月30日
@version 1.0
'''
from django.conf.urls import url
from . import views

app_name = "picture_process"
urlpatterns = [
    url(r'^zb/front/$', views.front_ps, name='front_ps'),
    url(r'^zb/data/$', views.data_ps, name='data_ps'),
    url(r'^zb/data_render/$', views.data_ps_get, name='data_ps_get'),
    url(r'^zb/query_base_url/$', views.query_base_url, name='query_base_url'),
    url(r'^zb/query_index_data/$', views.query_index_data, name='query_index_data'),
    url(r'^zb/index/$', views.front_index, name='front_index'),
]