import os
import random

from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from Admin.models import User, Manufacturer
import hashlib
from MyProduct import settings
import re


# Create your views here.
def show_manu(request):
    manus = Manufacturer.objects
    m_list = manus.all()
    context = {'manulist': m_list}
    return render(request, 'admin/manus/show.html', context)


def delete(request, m_id=0):
    del_manu = Manufacturer.objects.get(m_id=m_id)
    try:
        del_manu.m_status = 1
        del_manu.modifytime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        del_manu.save()
        context = {'info': "Manufacturer %s has been successfully removed." % del_manu.m_name,
                   'del_status': 1}

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Removing %s failed, Please try again." % del_manu.m_name,
                   'del_status': 0}
    return render(request, 'admin/users/delete.html', context)


def recovery(request, m_id=0):
    rec_manu = Manufacturer.objects.get(m_id=m_id)
    try:
        rec_manu.m_status = 0
        rec_manu.modifytime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rec_manu.save()
        context = {'info': "Information recovery succeeded",
                   'rec_status': 1}

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Information recovery failed, Please try again.",
                   'rec_status': 0}
    return render(request, 'admin/users/recovery.html', context)
