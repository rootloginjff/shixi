"""shixi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from user import urls as user_urls
from django.conf.urls import url,include
from rest_framework.documentation import  include_docs_urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/' , include(user_urls,namespace='user')),
    url(r'^docs/', include_docs_urls(title="my api site"))
]
