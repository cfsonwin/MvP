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
    path('', index.u_redirect, name='mU_redirect'),
    # homepage
    path('uid?<int:u_id>', index.index, name='mU_index'),
    # product
    path('uid?<int:u_id>/product/', products.show_all, name='mU_p_show'),
    path('uid?<int:u_id>/product/add', products.add_new_product, name='mU_p_add'),
    path('uid?<int:u_id>/product/insert', products.insert_new_product, name='mU_p_insert'),
    path('uid?<int:u_id>/product/insert?p_id=<int:p_id>', products.insert_cpmapping, name='mU_p_insert_cpmapping'),
    path('uid?<int:u_id>/product/view/<int:p_id>', products.show_details, name='mU_p_view'),
    path('uid?<int:u_id>/product/view2/<int:p_id>', products.show_details_2, name='mU_p_view2'),
    path('uid?<int:u_id>/product/view2/<int:p_id>?<int:m_id>', products.iframe, name='mU_p_iframe'),
    path('uid?<int:u_id>/product/jumpto', products.jump_to, name='mU_p_jumpto'),
    path('uid?<int:u_id>/product/edit/<int:p_id>', products.edit, name='mU_p_edit'),
    path('uid?<int:u_id>/product/edit/<int:p_id>/select', products.add_new_manu_select, name='mU_p_edit_select'),
    path('uid?<int:u_id>/product/edit/<int:p_id>/add', products.add_new_manu, name='mU_p_edit_add'),
    path('uid?<int:u_id>/product/edit/<int:p_id>/insert', products.insert_new_manu, name='mU_p_edit_insert'),
    path('uid?<int:u_id>/product/edit/<int:p_id>/insert?m_id=<int:m_id>&pnode=<int:m_pnode>',
         products.insert_pmmapping_new,
         name='mU_p_edit_insert_pmmapping_new'),
    path('uid?<int:u_id>/product/edit/<int:p_id>/insert?method=exist', products.insert_pmmapping_exist,
         name='mU_p_edit_insert_pmmapping_exist'),
    path('uid?<int:u_id>/product/update/<int:p_id>', products.updated, name='mU_p_update'),
    # Sign in
    path('signin/', index.signin_form, name='mU_signin'),
    path('dosignin/', index.do_signin, name='mU_dosignin'),
    path('signout/', index.sign_out, name='mU_signout'),
    path('signup/', index.signup, name='mU_signup'),
    path('signupcheck/', index.signup_check, name='mU_signupcheck'),
]
