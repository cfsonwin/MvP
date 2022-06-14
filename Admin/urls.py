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

from Admin.views import ad_index, ad_users, ad_products, ad_manus

urlpatterns = [
    # homepage
    path('', ad_index.index, name='mAD_index'),

    # user urls
    path('user/', ad_users.show, name='mAD_user'),
    path('user/add', ad_users.add, name='mAD_add'),
    path('user/insert', ad_users.insert, name='mAD_insert'),
    path('user/del/<int:u_id>', ad_users.delete, name='mAD_del'),
    path('user/recovery/<int:u_id>', ad_users.recovery, name='mAD_rec'),
    path('user/edit/<int:u_id>', ad_users.edit, name='mAD_edit'),
    path('user/update/<int:u_id>', ad_users.updated, name='mAD_update'),

    # manufacturer urls
    path('manu/', ad_manus.show_manu, name='mAD_manu'),
    path('manu/del/<int:m_id>', ad_manus.delete, name='mAD_manu_del'),
    path('manu/recovery/<int:m_id>', ad_manus.recovery, name='mAD_manu_rec'),

    # product
    path('product/', ad_products.show_all, name='mAD_p_show'),
    path('product/view/<int:p_id>', ad_products.show_details_2, name='mAD_p_view'),
    path('product/edit/<int:p_id>', ad_products.edit, name='mAD_p_edit'),
    path('product/update/<int:p_id>', ad_products.updated, name='mAD_p_update'),

    # Sign in
    path('signin/', ad_index.signin_form, name='mAD_signin'),
    path('dosignin/', ad_index.do_signin, name='mAD_dosignin'),
    path('signout/', ad_index.sign_out, name='mAD_signout'),
    path('signup/', ad_index.signup, name='mAD_signup'),
    path('signupcheck/', ad_index.signup_check, name='mAD_signupcheck'),
]
