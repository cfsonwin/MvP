import hashlib
import random
import re

from django.shortcuts import render, redirect
from django.urls import reverse

from Admin.models import Administrator
from Admin.utils import pw_hash_salt


# Create your views here.
def index(request):
    return render(request, 'admin/ad_index.html')


def do_signin(request):
    try:
        Ad = Administrator.objects.get(Email=request.POST['inputEmail'])
        if Ad.u_status != 0:
            context = {
                "info": "login failed! Administrator account not available, please contact with Super-Administrator",
                "status": 0,
                }
            return render(request, 'admin/admin_signin.html', context)
        if Ad.u_password == pw_hash_salt(request.POST['inputPassword'], Ad.pw_salt):
            request.session['already_login_ad'] = Ad.toDict()
            return redirect(reverse('mAD_index'))
        else:
            context = {"info": "login failed! Email account not exist or password wrong.",
                       "status": 0,
                       }
            return render(request, 'admin/admin_signin.html', context)
    except Exception as err:
        print(err)
        context = {"info": "login failed! Email account not exist or password wrong.",
                   "status": 0,
                   }
        return render(request, 'admin/admin_signin.html', context)


def signin_form(request):
    print(request.session.get('already_login_user'))
    print(request.session.get('already_login_ad'))
    print(request.session.get('already_login_manu'))
    return render(request, 'admin/admin_signin.html')


def sign_out(request):
    request.session.clear()
    return redirect(reverse('mAD_signin'))


def signup(request):
    return render(request, 'admin/admin_signup.html')


def signup_check(request):
    try:
        msg = []
        new_Admin = Administrator()
        u_firstname = request.POST['V_FirstName']
        u_lastname = request.POST['V_LastName']
        new_Admin.u_name = '%s/%s' % (u_firstname, u_lastname)
        if len(Administrator.objects.filter(Email=request.POST['V_Email'])) != 0:
            msg.append('This Email address is not available')
        new_Admin.Email = request.POST['V_Email']
        md5 = hashlib.md5()
        ran_n = random.randint(100000, 999999)
        new_pass = request.POST['V_Password'] + str(ran_n)
        md5.update(new_pass.encode('utf-8'))
        pattern = re.compile("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,20}$")
        if not pattern.match(request.POST['V_Password']):
            msg.append('Your password must be 8-20 characters long, contain letters and numbers')
        new_Admin.u_password = md5.hexdigest()
        new_Admin.pw_salt = ran_n
        new_Admin.u_status = 1
        if len(msg) == 0:
            new_Admin.save()
            context = {'info': "Successfully added.",
                       'add_status': 1
                       }
        else:
            context = {'info': msg,
                       'add_status': 0
                       }
        return render(request, 'admin/admin_signup_check.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': ["Add new user failed!"],
                   'add_status': 0
                   }
        return render(request, 'admin/admin_signup_check.html', context)
