"""myboot URL Configuration

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
"""
from django.urls import path

from .views import index, iframe, select_test, get_select_info, chart_generate

urlpatterns = [
    # homepage
    path('', index, name='mT_index'),
    path('iframe?<int:uid>', iframe, name='mT_iframe'),
    path('select', select_test, name='mT_select'),
    path('select_show', get_select_info, name='mT_get_select_info'),
    path('chart_generate', chart_generate, name='mT_chart'),

]
