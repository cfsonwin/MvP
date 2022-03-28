"""Users URL Configuration

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
from User.views import index, products
urlpatterns = [
    # homepage
    path('uid?<int:u_id>', index.index, name='mU_index'),
    # product
    path('uid?<int:u_id>/product/', products.show_all, name='mU_p_show'),
    path('uid?<int:u_id>/product/view/<int:p_id>', products.show_details, name='mU_p_view'),
    path('uid?<int:u_id>/product/edit/<int:p_id>', products.edit, name='mU_p_edit'),
    path('uid?<int:u_id>/product/update/<int:p_id>', products.updated, name='mU_p_update'),
    # Sign in
    path('signin/', index.signin_form, name='mU_signin'),
    path('dosignin/', index.do_signin, name='mU_dosignin'),
    path('signout/', index.sign_out, name='mU_signout'),
    path('signup/', index.signup, name='mU_signup'),
    path('signupcheck/', index.signup_check, name='mU_signupcheck'),
]
