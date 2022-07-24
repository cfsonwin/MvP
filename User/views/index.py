import hashlib
import random
import re
from datetime import datetime
import numpy as np
from django.shortcuts import render, redirect
from django.urls import reverse
from geopy import Nominatim

from Admin.models import User, CPmapping, Product, PMmapping, Manufacturer
from Admin.utils import pw_hash_salt

# Create your views here.
"""
Here are all the functions for rendering:
    User Login/Logout;
    User Sign up;
    User Homepage;
"""


def u_redirect(request):
    return redirect(reverse('mU_signin'))


def reply_form(request, u_id, pm_id):
    """
    Direct to the webpage for add a reply
    """
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    pm_record = PMmapping.objects.get(id=pm_id)
    m = Manufacturer.objects.get(m_id=pm_record.m_id)
    user = User.objects.get(u_id=u_id)
    m_name = m.m_name
    context = {
        'pm_id': pm_id,
        'm_name': m_name,
        'user': user,
        'name': hi_name,
    }

    return render(request, 'user/add_reply.html', context)


def mU_reply_insert(request, u_id, pm_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    pm_record = PMmapping.objects.get(id=pm_id)
    reply = request.POST.get('fb_reply')
    print(reply)

    pm_record.status = 0
    old_feedback = pm_record.feedback
    new_feedback = old_feedback + reply + ';;;'
    pm_record.feedback = new_feedback
    pm_record.save()
    return redirect(reverse('mU_index', kwargs={'u_id': u_id}))


def index(request, u_id):
    user = User.objects.get(u_id=u_id)
    products = CPmapping.objects.filter(c_id=u_id)
    pid_list = []
    p_name_list = []
    m_list = []
    chart_1_info = []
    add_year_list = []
    for product in products:
        p_id = product.p_id
        pid_list.append(p_id)
        _product = Product.objects.get(p_id=p_id)
        p_name_list.append(_product.p_name)
        _m_list = []
        manus = PMmapping.objects.filter(p_id=p_id)
        counter_all = 0
        counter_modified = 0
        # _add_year_list = []
        for manu in manus:
            counter_all += 1
            m_id = manu.m_id
            _m_list.append(m_id)
            add_time = manu.add_time
            modify_time = manu.modify_time
            add_year = int(add_time.year)
            if add_year not in [x[0] for x in add_year_list]:
                add_year_list.append([add_year, 0])
            if add_time != modify_time:
                counter_modified += 1
        chart_1_info.append([counter_all, counter_modified])
        m_list.append(_m_list)
    feedbacks_record = PMmapping.objects.filter(status=4).filter(p_id__in=pid_list)
    needvalid_record = PMmapping.objects.filter(status=2).filter(p_id__in=pid_list)
    needvalid_list = []
    for record in needvalid_record:
        record_id = record.id
        _p = Product.objects.get(p_id=record.p_id)
        msg1 = _p.p_name
        _m = Manufacturer.objects.get(m_id=record.m_id)
        msg2 = _m.m_name
        _pnode = record.m_pnode
        if int(_pnode) == 0:
            msg3 = "Get from you directly"
        else:
            _PManu = Manufacturer.objects.get(m_id=_pnode)
            msg3 = _PManu.m_name
        needvalid_list.append([record_id, msg1, msg2, msg3])
    for pid in pid_list:
        _records = PMmapping.objects.filter(p_id=pid)
        for record in _records:
            if int(record.status) == 0:
                pass
            elif int(record.status) == 4:
                pass
    feedback_table_list = []
    for record in feedbacks_record:
        id = record.id
        _p_id = record.p_id
        _p = Product.objects.get(p_id=_p_id)
        _m = Manufacturer.objects.get(m_id=record.m_id)
        _p_name = _p.p_name
        _m_name = _m.m_name
        feedback = record.feedback
        new_feedback = 'No Feedback'
        if ';;;' not in feedback:
            new_feedback = feedback.split('::')[0]
        else:
            i = 0
            while feedback.split(';;;')[i] != '':
                _feedback = feedback.split(';;;')[i]
                if feedback.split(';;;')[i].split('::')[1] == '':
                    new_feedback = feedback.split(';;;')[i].split('::')[0]
                    break
                i += 1
        feedback_table_list.append([id, _p_id, _p_name, _m_name, new_feedback])
    if len(add_year_list) == 0:
        add_year_list = [[0, 0]]
    data = np.array(add_year_list)
    data = data[np.argsort(data[:, 0])]
    sum_dict = {}
    for item in data:
        sum_dict[item[0]] = item[1]
    for product in products:
        p_id = product.p_id
        manus = PMmapping.objects.filter(p_id=p_id)
        for manu in manus:
            add_time = manu.add_time
            add_year = int(add_time.year)
            for key in sum_dict.keys():
                if key >= add_year:
                    sum_dict[key] += 1
    context = {
        "user": user,
        'test': 'test',
        'info': chart_1_info,
        'p_list': p_name_list,
        'info2': sum_dict,
        'name': user.u_name.split('/')[0],
        'u_lastname': user.u_name.split('/')[1],
        'needvalid_list': needvalid_list,
        'feedback_table_list': feedback_table_list,
    }
    return render(request, 'user/user_index.html', context)


def request_agree(request, u_id, pm_id):
    record = PMmapping.objects.get(id=pm_id)
    record.status = 0
    record.save()
    return redirect(reverse('mU_index', kwargs={'u_id': u_id}))


def request_refuse(request, u_id, pm_id):
    record = PMmapping.objects.get(id=pm_id)
    record.status = 1
    record.save()
    return redirect(reverse('mU_index', kwargs={'u_id': u_id}))


def do_signin(request):
    try:
        user = User.objects.get(Email=request.POST['inputEmail'])
        u_login_list = []
        if user.u_status != 0:
            context = {
                "info": "login failed! Account not available, please contact with Super-Administrator",
                "status": 0,
            }
            return render(request, 'user/user_signin.html', context)
        if user.u_password == pw_hash_salt(request.POST['inputPassword'], user.pw_salt):
            if request.session.get('already_login_user'):
                u_login_list = request.session.get('already_login_user')['u_id']
                if user.u_id not in u_login_list:
                    u_login_list.append(user.u_id)
                request.session['already_login_user'] = {'u_id': u_login_list}
            else:
                u_login_list.append(user.u_id)
                request.session['already_login_user'] = {'u_id': u_login_list}

            return redirect(reverse('mU_index', kwargs={'u_id': user.u_id}))
        else:
            print(user.u_name)
            print(user.u_password)
            print(pw_hash_salt(request.POST['inputPassword'], user.pw_salt))
            context = {"info": "login failed! Email account not exist or password wrong.",
                       "status": 0,
                       }
            return render(request, 'user/user_signin.html', context)
    except Exception as err:
        print("cc")
        print(err)
        context = {"info": "login failed! Email account not exist or password wrong.",
                   "status": 0,
                   }
        return render(request, 'user/user_signin.html', context)


def signin_form(request):
    print(request.session.get('already_login_user'))
    print(request.session.get('already_login_ad'))
    print(request.session.get('already_login_manu'))
    return render(request, 'user/user_signin.html')


def sign_out(request):
    # request.session.clear()
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
        if request.POST['select_method'] == "AddManually":
            addr = '%s, %s, %s, %s' % (
                request.POST['Address'],
                request.POST['Zip'],
                request.POST['City'],
                request.POST['State']
            )
            new_user.addr = addr
            loc = '%s,%s' % (
                request.POST['lat'],
                request.POST['lon']
            )
            new_user.loc = loc
        elif request.POST['select_method'] == "SelectFromMap":
            geolocator = Nominatim(user_agent="get_location")
            latitude = request.POST['lat_fm']
            longitude = request.POST['lon_fm']
            loc = '%s,%s' % (
                latitude,
                longitude
            )
            new_user.loc = loc
            location = geolocator.reverse((latitude, longitude))
            addr = location.address
            new_user.addr = addr
        else:
            msg.append('Error occurred by getting location')
        new_user.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
