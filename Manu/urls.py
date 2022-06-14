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

from Manu.views import manu_index, m_products

urlpatterns = [
    # homepage
    path('mid?<int:m_id>', manu_index.index, name='mM_index'),

    # add new product
    path('mid?<int:m_id>/select_product', m_products.select_a_product, name='mM_p_select'),
    path('mid?<int:m_id>/select_pnode', m_products.select_a_pnode, name='mM_pnode_select'),
    path('mid?<int:m_id>/warning', m_products.warning, name='mM_warning'),
    path('mid?<int:m_id>/add_pmmapping/p_id?<int:p_id>', m_products.add_pmmapping, name='mM_add_pmmapping'),

    # view
    path('mid?<int:m_id>/view/p_id?<int:p_id>', m_products.view, name='mM_view'),
    path('mid?<int:m_id>/view/jump_to', m_products.jump_to, name='mM_p_jumpto'),
    path('mid?<int:m_id>/view/add_log_for_p_id?<int:p_id>', m_products.add_log, name='mM_addlog'),
    path('mid?<int:m_id>/view/add_ProducingPeriod_for_p_id?<int:p_id>', m_products.addProducingPeriod,
         name='mM_addProducingPeriod'),
    path('mid?<int:m_id>/view/mStatusUpdate_for_p_id?<int:p_id>', m_products.mStatusUpdate,
         name='mM_StatusUpdate'),
    # feedback
    path('mid?<int:m_id>/feedback/p_id?<int:p_id>', m_products.feedback, name='mM_feedback'),
    path('mid?<int:m_id>/feedback/insert/p_id?<int:p_id>', m_products.insert_feedback, name='mM_insert_feedback'),

    # sign in
    path('signin/', manu_index.signin_form, name='mM_signin'),
    path('dosignin/', manu_index.do_signin, name='mM_dosignin'),
    path('signout/', manu_index.sign_out, name='mM_signout'),
    path('signup/', manu_index.signup, name='mM_signup'),
    path('signupcheck/', manu_index.signup_check, name='mM_signupcheck'),

]
