from django.contrib import admin
from django.urls import path ,include
from web_tool import views 

#用來決定網址名稱
urlpatterns = [
    path("admin/", admin.site.urls),
    path('web_tool/', include('web_tool.urls')),

]
