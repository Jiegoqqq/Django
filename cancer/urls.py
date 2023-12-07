from django.urls import path,re_path
from . import views

urlpatterns = [
    path('cancer_web/', views.cancer_web),
    path('cancer_data/', views.cancer_data),
    path('gene_name_data/', views.gene_name_data),
    path('cancer_plot_data/', views.cancer_plot_data),
    path('cancer_screener_web/', views.cancer_screener_web),
    path('cancer_screener_data/', views.cancer_screener_data),
    re_path(r'cancer_web/(?P<id>.+)',views.cancer_web),

]