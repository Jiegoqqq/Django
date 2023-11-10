from django.urls import path,re_path
from . import views

urlpatterns = [
    path('hello/',views.hello_world),
    path('', views.index),
    path('form/', views.form),
    path('ajax_data/', views.ajax_data), #設給javascript用的
    path('transcript/',views.transcript),
    path('pirScan_data/',views.pirScan_data),
    path('function_list/',views.function_list),
    path('filter/',views.filter),
    path('filter_data/',views.filter_data),
    path('search_data/',views.search_data),
    path('search_data2/',views.search_data2),
    path('read_count_data/',views.read_count_data),
    path('read_count_data2/',views.read_count_data2),    
    re_path(r'table/(?P<id>.+)',views.table), #設給點擊超連結用的 用正則表達式且id代表點擊的transcript id
    re_path(r'pirscan/(?P<id>.+)',views.pirScan),
    re_path(r'search/(?P<id>.+)',views.search),
    re_path(r'read_count/(?P<id>.+)',views.read_count),


    
]