import os
import random

from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from Admin.models import User
import hashlib
from MyProduct import settings
import re
# Create your views here.
def show(request):
    users = User.objects
    u_list = users.all()
    context = {'userlist': u_list}
    return render(request, 'admin/users/show.html', context)


def add(request):
    return render(request, 'admin/users/add.html')


def insert(request):
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
        # print(type(request.FILES['avatar']))
        # pic = request.FILES['avatar']
        # # print(pic)
        # save_path = '%s/%s_avatar.%s' % (os.path.join(settings.STATICFILES_DIRS[0], 'user_avatar'),
        #                                  request.POST['email'].split('.')[0],
        #                                  pic.name.split('.')[-1])
        # with open(save_path, 'wb') as f:
        #     for content in pic.chunks():
        #         f.write(content)
        # new_user.avatar = save_path
        addr = '%s_%s_%s_%s' % (
            request.POST['Address'],
            request.POST['Zip'],
            request.POST['City'],
            request.POST['State']
        )
        new_user.addr = addr
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
        return render(request, 'admin/users/insert.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': ["Add new user failed!"],
                   'add_status': 0
                   }
        return render(request, 'admin/users/insert.html', context)


def delete(request, u_id=0):
    print(u_id)
    del_user = User.objects.get(u_id=u_id)
    try:
        del_user.u_status = 1
        del_user.modifytime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        del_user.save()
        context = {'info': "User %s has been successfully removed." % del_user.Email,
                   'add_status': 1}

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Removing %s failed, Please try again." % del_user.Email,
                   'add_status': 0}
    return render(request, 'admin/users/delete.html', context)


def recovery(request, u_id=0):
    print(u_id)
    del_user = User.objects.get(u_id=u_id)
    try:
        del_user.u_status = 0
        del_user.modifytime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        del_user.save()
        context = {'info': "Information recovery succeeded",
                   'add_status': 1}

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Information recovery failed, Please try again.",
                   'add_status': 0}
    return render(request, 'admin/users/recovery.html', context)


def edit(request, u_id=0):
    edit_user = User.objects.get(u_id=u_id)
    print(u_id)
    try:
        context = {'edit_user': edit_user,
                   'u_id': u_id,
                   'u_firstname': edit_user.u_name.split('/')[0],
                   'u_lastname': edit_user.u_name.split('/')[1],
                   'Address': edit_user.addr.split('_')[0],
                   'Zip': edit_user.addr.split('_')[1],
                   'City': edit_user.addr.split('_')[2],
                   'State': edit_user.addr.split('_')[3],
        }
        return render(request, 'admin/users/edit.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later."}
        return render(request, 'admin/users/info.html', context)


def updated(request, u_id):
    edit_user = User.objects.get(u_id=u_id)
    try:
        u_firstname = request.POST['u_firstname']
        u_lastname = request.POST['u_lastname']
        edit_user.u_name = '%s/%s' % (u_firstname, u_lastname)
        addr = '%s_%s_%s_%s' % (
            request.POST['Address'],
            request.POST['Zip'],
            request.POST['City'],
            request.POST['State']
        )
        edit_user.addr = addr
        edit_user.modifytime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_user.save()
        context = {'info': "Information for user %s has been successfully updated" % edit_user.Email,
                   'update_status': 1,
                   'u_id': u_id
                   }
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later.",
                   'update_status': 0,
                   'u_id': u_id
                   }
    return render(request, 'admin/users/update.html', context)
