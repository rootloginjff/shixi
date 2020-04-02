app_name = 'user'
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index/',views.index,name='index'),
    url(r'^login/',views.PhonePasswordLoginApiView.as_view(),name='login'),
    url(r'^register/',views.PhoneCodeRegisterCreateAPIView.as_view(),name='register'),
    url(r'^logout/',views.logoutAPIView.as_view(),name='logout'),
    url(r'^codelogin/',views.phonecodeloginApiView.as_view(),name='code'),
    url(r'^sendcode/',views.phonesendcodeApiView.as_view(),name="sendcode")
]