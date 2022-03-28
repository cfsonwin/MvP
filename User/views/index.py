import hashlib
import random
import re
from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse

from Admin.models import User
from Admin.utils import pw_hash_salt


# Create your views here.
def index(request, u_id):
    print('xxxxxxxxxxxx', u_id)
    user = User.objects.get(u_id=u_id)

    context = {
        "user": user,
        'u_firstname': user.u_name.split('/')[0],
        'u_lastname': user.u_name.split('/')[1],

    }
    return render(request, 'user/user_index.html', context)


def do_signin(request):
    try:
        user = User.objects.get(Email=request.POST['inputEmail'])
        if user.u_status != 0:
            context = {
                "info": "login failed! Account not available, please contact with Super-Administrator",
                "status": 0,
                }
            return render(request, 'user/user_signin.html', context)
        if user.u_password == pw_hash_salt(request.POST['inputPassword'], user.pw_salt):
            print(user.u_id)
            # request.session['already_login_user'] = user.toDict()
            return redirect(reverse('mU_index', kwargs={'u_id': user.u_id}))
        else:
            context = {"info": "login failed! Email account not exist or password wrong.",
                       "status": 0,
                       }
            return render(request, 'user/user_signin.html', context)
    except Exception as err:
        print(err)
        context = {"info": "login failed! Email account not exist or password wrong.",
                   "status": 0,
                   }
        return render(request, 'user/user_signin.html', context)


def signin_form(request):
    return render(request, 'user/user_signin.html')


def sign_out(request):
    del request.session['already_login_user']
    return redirect(reverse('mU_signin'))


def signup(request):
    return render(request, 'user/user_signup.html')


def signup_check(request):
    try:
        msg = []
        new_user = User()
        u_firstname = request.POST['u_firstname']
        u_lastname = request.POST['u_lastname']
        new_user.u_name = '%s/%s' % (u_firstname, u_lastname)
        if len(User.objects.filter(Email=request.POST['email'])) != 0:
            msg.append('This Email address is not available')
        new_user.Email = request.POST['email']
        md5 = hashlib.md5()
        ran_n = random.randint(100000, 999999)
        new_pass = request.POST['u_pw'] + str(ran_n)
        md5.update(new_pass.encode('utf-8'))
        pattern = re.compile("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,20}$")
        if not pattern.match(request.POST['u_pw']):
            msg.append('Your password must be 8-20 characters long, contain letters and numbers')
        new_user.u_password = md5.hexdigest()
        new_user.pw_salt = ran_n
        addr = '%s_%s_%s_%s' % (
            request.POST['Address'],
            request.POST['Zip'],
            request.POST['City'],
            request.POST['State']
        )
        new_user.addr = addr
        new_user.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user.modifytime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user.u_status = 0
        if len(msg) == 0:
            new_user.save()
            context = {'info': "Successfully added.",
                       'add_status': 1
                       }
        else:
            context = {'info': msg,
                       'add_status': 0
                       }
        return render(request, 'user/user_signup_check.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': ["Add new user failed!"],
                   'add_status': 0
                   }
        return render(request, 'user/user_signup_check.html', context)


