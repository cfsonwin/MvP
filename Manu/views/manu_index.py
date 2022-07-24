import hashlib
import random
import re
from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from geopy.geocoders import Nominatim

from Admin.models import Manufacturer, PMmapping, Product
from Admin.utils import pw_hash_salt


# Create your views here.


def index(request, m_id):
    Manu = Manufacturer.objects.get(m_id=m_id)
    products = PMmapping.objects.filter(m_id=m_id)
    productlist_valid = []
    productlist_need_validation = []
    productlist_not_valid = []
    for product in products:
        if int(product.status) == 0 or int(product.status) == 4:
            _product = Product.objects.get(p_id=product.p_id)
            productlist_valid.append(_product)
        elif int(product.status) == 2:
            _product = Product.objects.get(p_id=product.p_id)
            productlist_need_validation.append(_product)
        else:
            _product = Product.objects.get(p_id=product.p_id)
            productlist_not_valid.append(_product)
    context = {
        'm_id': m_id,
        'productlist_activ': productlist_valid,
        'productlist_need_validation': productlist_need_validation,
        'productlist_not_valid': productlist_not_valid,
        'name': Manu.m_name,
    }
    return render(request, 'manu/manu_index.html', context)


def do_signin(request):
    try:
        manu = Manufacturer.objects.get(contact=request.POST['inputEmail'])
        m_login_list = []
        if manu.m_status != 0:
            context = {
                "info": "login failed! Account not available, please contact with Super-Administrator",
                "status": 0,
            }
            return render(request, 'manu/manu_signin.html', context)
        if manu.m_password == pw_hash_salt(request.POST['inputPassword'], manu.pw_salt):
            if request.session.get('already_login_manu'):
                m_login_list = request.session.get('already_login_manu')['m_id']
                if manu.m_id not in m_login_list:
                    m_login_list.append(manu.m_id)
                request.session['already_login_manu'] = {'m_id': m_login_list}
            else:
                m_login_list.append(manu.m_id)
                request.session['already_login_manu'] = {'m_id': m_login_list}

            return redirect(reverse('mM_index', kwargs={'m_id': manu.m_id}))
        else:
            context = {"info": "login failed! Email account not exist or password wrong.",
                       "status": 0,
                       }
            return render(request, 'manu/manu_signin.html', context)
    except Exception as err:
        print(err)
        context = {"info": "login failed! Email account not exist or password wrong.",
                   "status": 0,
                   }
        return render(request, 'manu/manu_signin.html', context)


def signin_form(request):
    print(request.session.get('already_login_manu'))
    return render(request, 'manu/manu_signin.html')


def sign_out(request):
    # request.session.clear()
    del request.session['already_login_manu']
    return redirect(reverse('mM_signin'))


def signup(request):
    return render(request, 'manu/manu_signup.html')


def signup_check(request):
    try:
        msg = []
        new_manu = Manufacturer()
        new_manu.m_name = request.POST['m_name']
        if len(Manufacturer.objects.filter(contact=request.POST['m_email'])) != 0:
            msg.append('This Email address is not available')
        new_manu.contact = request.POST['m_email']
        new_manu.description = request.POST['m_description']
        md5 = hashlib.md5()
        ran_n = random.randint(100000, 999999)
        new_pass = request.POST['m_pw'] + str(ran_n)
        md5.update(new_pass.encode('utf-8'))
        pattern = re.compile("^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,20}$")
        if not pattern.match(request.POST['m_pw']):
            msg.append('Your password must be 8-20 characters long, contain letters and numbers')
        new_manu.m_password = md5.hexdigest()
        new_manu.pw_salt = ran_n
        # two method for addr add
        print(request.POST['select_method'])
        if request.POST['select_method'] == "AddManually":
            addr = '%s, %s, %s, %s' % (
                request.POST['Address'],
                request.POST['Zip'],
                request.POST['City'],
                request.POST['State']
            )
            new_manu.addr = addr
            loc = '%s,%s' % (
                request.POST['lat'],
                request.POST['lon']
            )
            new_manu.loc = loc
        elif request.POST['select_method'] == "SelectFromMap":
            geolocator = Nominatim(user_agent="get_location")
            latitude = request.POST['lat_fm']
            longitude = request.POST['lon_fm']
            loc = '%s,%s' % (
                latitude,
                longitude
            )
            new_manu.loc = loc
            location = geolocator.reverse((latitude, longitude))
            addr = location.address
            new_manu.addr = addr
        else:
            msg.append('Error occurred by getting location')
        new_manu.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_manu.m_status = 0

        if len(msg) == 0:
            new_manu.save()
            context = {'info': "Successfully Sign up.",
                       'add_status': 1
                       }
        else:
            context = {'info': msg,
                       'add_status': 0
                       }
        return render(request, 'manu/manu_signup_check.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': ["Add new user failed!"],
                   'add_status': 0
                   }
        return render(request, 'manu/manu_signup_check.html', context)




