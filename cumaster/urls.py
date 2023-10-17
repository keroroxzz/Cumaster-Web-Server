'''cumaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
'''
from django.contrib import admin
from django.urls import include, path

import gamecore.views as views

import gamecore, pages

admin.autodiscover()

from django.http import HttpResponse
def handler404(request, exception):
    return HttpResponse("ERROR 404: Page not found!")

def handler500(request):
    return HttpResponse("ERROR 500: Server error")

urlpatterns = [
    path('', include('pages.urls')),
    path('gamecore/', include('gamecore.urls')),
    #path('admin/', admin.site.urls),
    path('404/', handler404),
    path('500/', handler500),
]
