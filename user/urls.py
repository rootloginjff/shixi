app_name = 'user'
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'index/',views.index,name='index'),
    url(r'login/',views.userlogin,name='login')
]