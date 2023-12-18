from django.contrib import admin
from django.urls import path ,include
from web_tool import views 

# from django.conf.urls import url, include
from rest_framework import routers
from table_api import views


router1 = routers.DefaultRouter()
router1.register(r'', views.UPDATEGENEANNOTATIONViewSet, basename="update_GeneAnnotation")



#用來決定網址名稱
urlpatterns = [
    path("admin/", admin.site.urls),
    path('web_tool/', include('web_tool.urls')),
    path('web_tool/', include('cancer.urls')),
    path('web_tool/', include('table_api.urls')),

    path(r'update_GeneAnnotation/', include(router1.urls)),
]


