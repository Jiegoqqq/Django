from django.urls import path,re_path
from . import views

urlpatterns = [
    path('table_api_web/', views.table_api_web),

]