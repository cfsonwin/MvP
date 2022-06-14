import hashlib
import random
import re
from datetime import datetime

from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from geopy import Nominatim

from Admin.models import Product, CPmapping, User, PMmapping, Manufacturer
from Admin.utils import Manus, LineInfo, get_search_id
from User.utils import get_centroid


def get_loc_dict(manufacturers):
    loc_dic = {}
    line_dic = {}
    for manufacturer in manufacturers:
        if manufacturer.m_pnode == 0:
            this_manu = Manufacturer.objects.get(m_id=manufacturer.m_id)
            loc_dic[this_manu.m_id] = Manus(
                this_manu,
                manufacturer,
                "Direct get from product constructor",
            )
        elif manufacturer.m_pnode != 0:
            this_manu = Manufacturer.objects.get(m_id=manufacturer.m_id)
            lat = float(this_manu.loc.split(',')[0])
            lon = float(this_manu.loc.split(',')[1])
            lat_p = float(Manufacturer.objects.get(m_id=manufacturer.m_pnode).loc.split(',')[0])
            lon_p = float(Manufacturer.objects.get(m_id=manufacturer.m_pnode).loc.split(',')[1])
            line = LineInfo(lat, lon, lat_p, lon_p)
            line_dic[this_manu.m_id] = line
            loc_dic[this_manu.m_id] = Manus(
                this_manu,
                manufacturer,
                "Get from %s" % Manufacturer.objects.get(m_id=manufacturer.m_pnode).m_name,
            )
    return line_dic, loc_dic


# Create your views here.
def show_all(request, u_id):
    print(request.session.get('already_login_user'))
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    products = CPmapping.objects.filter(c_id=u_id)
    product_list = []
    for product in products:
        product_list.append(Product.objects.get(p_id=product.p_id))

    context = {'productlist': product_list,
               'u_id': u_id,
               'name': hi_name,
               }
    return render(request, 'user/products/show.html', context)


def jump_to(request, u_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    p_id = request.POST['p_id_selected']
    return redirect(reverse('mU_p_view2', kwargs={'u_id': u_id, 'p_id': p_id}))


def show_details_2(request, u_id, p_id=0):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    product = Product.objects.get(p_id=p_id)
    owners = CPmapping.objects.filter(p_id=p_id)
    valid_status = [0, 4]
    need_valid_status = [2]
    no_valid_status = [1]
    manufacturers_valid = PMmapping.objects.filter(p_id=p_id).filter(status__in=valid_status)
    manufacturers_need_valid = PMmapping.objects.filter(p_id=p_id).filter(status__in=need_valid_status)
    manufacturers_no_valid = PMmapping.objects.filter(p_id=p_id).filter(status__in=no_valid_status)
    manufacturers = PMmapping.objects.filter(p_id=p_id)
    products = CPmapping.objects.filter(c_id=u_id)
    p_id_list = []
    for p in products:
        p_id_list.append(p.p_id)
    P_list = Product.objects.filter(p_id__in=p_id_list).exclude(p_id=p_id)

    u_list = []
    try:
        class Info:
            def __init__(self, loc, p_id):
                self.loc = loc
                self.p_id = p_id

        for owner in owners:
            u_list.append(owner.c_id)
        line_dic_need_valid, loc_dic_need_valid = get_loc_dict(manufacturers_need_valid)
        line_dic_no_valid, loc_dic_no_valid = get_loc_dict(manufacturers_no_valid)
        line_dic, loc_dic = get_loc_dict(manufacturers_valid)
        line_dic_all, loc_dic_all = get_loc_dict(manufacturers)
        users = User.objects.filter(u_id__in=u_list)
        user_dic = {}
        for user in users:
            first_name = user.u_name.split('/')[0]
            family_name = user.u_name.split('/')[1]
            user_dic['%s %s' % (first_name, family_name)] = user.Email
        if len(loc_dic.keys()) == 0:
            lat = 49.861252
            lon = 8.682602
            zoom_index = 6
        else:
            latlon, zoom_index = get_centroid(loc_dic_all)
            lat = latlon[0]
            lon = latlon[1]
        context = {'loc_dic': loc_dic,
                   'u_id': u_id,
                   'p_id': p_id,
                   'user_dic': user_dic,
                   'lat': lat,
                   'lon': lon,
                   'line_dic': line_dic,
                   'zoom_index': zoom_index,
                   'add_status': 1,
                   'product': product,
                   'P_list': P_list,
                   'name': hi_name,
                   'line_dic_need_valid': line_dic_need_valid,
                   'loc_dic_need_valid': loc_dic_need_valid,
                   'line_dic_no_valid': line_dic_no_valid,
                   'loc_dic_no_valid': loc_dic_no_valid,
                   }

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Showing information for product %s failed, Please try again." % product.p_name,
                   'u_id': u_id,
                   'p_id': p_id,
                   'add_status': 0,
                   'name': hi_name, }
    return render(request, 'user/products/view2.html', context)


def iframe(request, u_id, p_id, m_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    product = Product.objects.get(p_id=p_id)
    try:
        # owners = CPmapping.objects.filter(p_id=p_id)
        manufacturer = PMmapping.objects.filter(p_id=p_id).get(m_id=m_id)
        feedback = manufacturer.feedback
        print(feedback)
        feedback_dic = {}
        if feedback == "No feedback":
            status_feedback = 0
            feedback_dic['No feedback'] = "No feedback"
        else:
            if manufacturer.status == 4:
                if ';;;' not in feedback:
                    feedback_dic[feedback.split('::')[0]] = feedback.split('::')[1]
                else:
                    i = 0
                    feedback_dic = {}
                    while feedback.split(';;;')[i] != '':
                        _feedback = feedback.split(';;;')[i]
                        feedback_dic[feedback.split(';;;')[i].split('::')[0]] = feedback.split(';;;')[i].split('::')[1]
                        if feedback.split(';;;')[i].split('::')[1] == '':
                            break
                        i += 1
                status_feedback = 2
            else:
                i = 0
                feedback_dic = {}
                while feedback.split(';;;')[i] != '':
                    feedback_dic[feedback.split(';;;')[i].split('::')[0]] = feedback.split(';;;')[i].split('::')[1]
                    if feedback.split(';;;')[i].split('::')[1] == '':
                        break
                    i += 1
                status_feedback = 1
        this_manu = Manufacturer.objects.get(m_id=manufacturer.m_id)
        if manufacturer.m_pnode == 0:
            info = Manus(
                this_manu,
                manufacturer,
                "Direct get from product constructor",
            )
        else:
            info = Manus(
                this_manu,
                manufacturer,
                "Get from %s" % Manufacturer.objects.get(m_id=manufacturer.m_pnode).m_name,
            )
        location_country = this_manu.addr.split(',')[-1]
        location_city = this_manu.addr.split(',')[-3]
        loca = location_country + ', ' + location_city
        context = {
            'u_id': u_id,
            'p_id': p_id,
            'm_id': m_id,
            'info': info,
            'status': 1,
            'name': hi_name,
            'status_feedback': status_feedback,
            'feedback_dic': feedback_dic,
            'loca': loca,
        }
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Showing information for product %s failed, Please try again." % product.p_name,
                   'u_id': u_id,
                   'status': 0,
                   'name': hi_name, }
    return render(request, 'user/products/iframe.html', context)


def edit(request, u_id, p_id=0):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    edit_product = Product.objects.get(p_id=p_id)
    # e_owners = CPmapping.objects.filter(p_id=p_id).exclude(c_id=u_id)
    e_owners = CPmapping.objects.filter(p_id=p_id)
    e_manufacturers = PMmapping.objects.filter(p_id=p_id)
    M_list = Manufacturer.objects.all()
    try:
        u_list = []
        line_dic, manus_dic = get_loc_dict(e_manufacturers)
        for owner in e_owners:
            u_list.append(owner.c_id)

        users = User.objects.filter(u_id__in=u_list)
        user_dic = {}
        for user in users:
            first_name = user.u_name.split('/')[0]
            family_name = user.u_name.split('/')[1]
            user_dic['%s %s' % (first_name, family_name)] = user.Email
        context = {'edit_product': edit_product,
                   'u_id': u_id,
                   'p_id': p_id,
                   'M_list': M_list,
                   'owners': users,
                   'manus_dic': manus_dic,
                   'user_dic': user_dic,
                   'name': hi_name,
                   }
        return render(request, 'user/products/edit.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later.",
                   'u_id': u_id,
                   'p_id': p_id,
                   'name': hi_name,
                   }
        return render(request, 'user/products/info.html', context)


def updated(request, u_id, p_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    edit_product = Product.objects.get(p_id=p_id)
    try:
        edit_discription = request.POST['p_discription']
        edit_name = request.POST['p_name']
        edit_product.description = edit_discription
        edit_product.p_name = edit_name
        if request.POST['ProductStatus'] == 'private':
            edit_product.p_status = 0
        elif request.POST['ProductStatus'] == 'public':
            edit_product.p_status = 1
        else:
            return Http404
        edit_product.save()
        context = {'info': "description for Product %s has been successfully updated" % edit_product.p_name,
                   'update_status': 1,
                   'p_id': p_id,
                   'u_id': u_id,
                   'name': hi_name,
                   }
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later.",
                   'update_status': 0,
                   'p_id': p_id,
                   'u_id': u_id,
                   'name': hi_name,
                   }
    return render(request, 'user/products/update.html', context)


def add_new_product(request, u_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    context = {
        'u_id': u_id,
        'name': hi_name,
    }
    return render(request, 'user/products/add_p.html', context)


def insert_new_product(request, u_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    try:
        msg = []
        new_product = Product()
        if len(Product.objects.filter(p_name=request.POST['p_name'])) != 0:
            msg.append('This name for your product is not available')
        p_name = request.POST['p_name']
        p_description = request.POST['p_description']
        new_product.p_name = p_name
        new_product.description = p_description
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_product.addtime = time_now
        if request.POST['ProductStatus'] == 'private':
            new_product.p_status = 0
        elif request.POST['ProductStatus'] == 'public':
            new_product.p_status = 1
        else:
            msg.append("please select a valid status for your product.")
        search_id = get_search_id(p_name, time_now)
        new_product.search_id = search_id
        if len(msg) == 0:
            new_product.save()
            new_p = Product.objects.get(p_name=p_name)
            context = {'info': "Successfully added.",
                       'add_status': 1,
                       'u_id': u_id,
                       'new_product': new_p,
                       'name': hi_name,
                       'search_id': search_id,
                       }
        else:
            context = {'info': msg,
                       'add_status': 0,
                       'u_id': u_id,
                       'name': hi_name,
                       }
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': ["Add new product failed!"],
                   'add_status': 0,
                   'u_id': u_id,
                   'name': hi_name,
                   }
    return render(request, 'user/products/insert_p.html', context)


def insert_cpmapping(request, u_id, p_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    try:
        msg = []
        new_map = CPmapping()
        user = User.objects.get(u_id=u_id)
        new_map.c_id = u_id
        new_map.p_id = p_id
        new_map.c_email = user.Email

        new_map.save()


    except Exception as err:
        print('***************')
        print(err)

    return redirect(reverse('mU_p_show', kwargs={'u_id': u_id}))


def add_new_manu_select(request, u_id, p_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    context = {
        'u_id': u_id,
        'p_id': p_id,
        'name': hi_name,
    }
    return render(request, 'user/products/m_select.html', context)


def add_new_manu(request, u_id, p_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    selected_method = int(request.POST['add_method_selected'])
    M_list_all = Manufacturer.objects.all()
    manufacturers = PMmapping.objects.filter(p_id=p_id)
    products = CPmapping.objects.filter(c_id=u_id)
    m_id_list = []
    for m in manufacturers:
        m_id_list.append(m.m_id)
    M_list = Manufacturer.objects.all().exclude(m_id__in=m_id_list)
    Pnode_list = Manufacturer.objects.all().filter(m_id__in=m_id_list)
    if selected_method == 1:
        context = {
            'M_list': M_list,
            'M_list_all': Pnode_list,
            'u_id': u_id,
            'p_id': p_id,
            'name': hi_name,
        }
        return render(request, 'user/products/add_exist_m.html', context)
    elif selected_method == 2:
        context = {
            'M_list': Pnode_list,
            'u_id': u_id,
            'p_id': p_id,
            'name': hi_name,
        }
        return render(request, 'user/products/add_new_m.html', context)
    else:
        return Http404


def insert_new_manu(request, u_id, p_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    try:
        m_pnode = int(request.POST['m_pid_selected'])
        m_name = request.POST['m_name']
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
            new_m = Manufacturer.objects.get(m_name=m_name)
            context = {'info': "Successfully added.",
                       'add_status': 1,
                       'u_id': u_id,
                       'p_id': p_id,
                       'new_manu': new_m,
                       'm_pnode': m_pnode,
                       'name': hi_name,
                       }
        else:
            context = {'info': msg,
                       'add_status': 0,
                       'p_id': p_id,
                       'u_id': u_id,
                       'name': hi_name,
                       }
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': ["Add new Manufacturer failed!"],
                   'add_status': 0,
                   'u_id': u_id,
                   'p_id': p_id,
                   'name': hi_name,
                   }
    return render(request, 'user/products/insert_new_m.html', context)


def insert_pmmapping_exist(request, u_id, p_id):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    try:

        m_id = request.POST['m_id_selected']
        new_map = PMmapping()
        new_map.p_id = p_id
        new_map.m_id = m_id
        m_pnode = int(request.POST['m_pid_selected'])
        if m_pnode == int(m_id):
            context = {
                'u_id': u_id,
                'p_id': p_id,
                'info': "The parent node of this manufacturer must be different!",
                'name': hi_name,
            }
            return render(request, 'user/products/info_2.html', context)

        if m_pnode == 0:
            new_map.m_pnode = 0
            new_map.m_Tlevel = 1
        else:
            new_map.m_pnode = m_pnode
            pnode_Tlevel = PMmapping.objects.filter(p_id=p_id).get(m_id=m_pnode).m_Tlevel
            new_map.m_Tlevel = int(pnode_Tlevel) + 1
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_map.add_time = time_now
        new_map.modify_time = time_now
        new_map.modify_log = "%s::First time added;;;" % time_now
        new_map.feedback = "No feedback"
        new_map.producing_period = "No record"
        new_map.save()

    except Exception as err:
        print('***************')
        print(err)

    return redirect(reverse('mU_p_view2', kwargs={'u_id': u_id, 'p_id': p_id}))


def insert_pmmapping_new(request, u_id, p_id, m_id, m_pnode):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    try:
        new_map = PMmapping()
        new_map.p_id = p_id
        new_map.m_id = m_id
        if m_pnode == m_id:
            context = {
                'u_id': u_id,
                'p_id': p_id,
                'info': "The parent node of this manufacturer must be diffrernt!",
                'name': hi_name,
            }
            return render(request, 'user/products/info_2.html', context)
        if m_pnode == 0:
            new_map.m_pnode = 0
            new_map.m_Tlevel = 1
        else:
            new_map.m_pnode = m_pnode
            pnode_Tlevel = PMmapping.objects.filter(p_id=p_id).get(m_id=m_pnode).m_Tlevel
            new_map.m_Tlevel = int(pnode_Tlevel) + 1
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_map.add_time = time_now
        new_map.modify_time = time_now
        new_map.modify_log = "%s::First time added;;;" % time_now
        new_map.feedback = "No feedback"
        new_map.producing_period = "No record"
        new_map.save()

    except Exception as err:
        print('***************')
        print(err)

    return redirect(reverse('mU_p_view2', kwargs={'u_id': u_id, 'p_id': p_id}))


def pm_delete(request, u_id=0, p_id=0, pm_id=0):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    del_pm = PMmapping.objects.get(id=pm_id)
    manu = Manufacturer.objects.get(m_id=del_pm.m_id)
    try:
        del_pm.status = 1
        del_pm.save()
        context = {'info': "Manufacturer %s has been successfully removed." % manu.m_name,
                   'del_status': 1,
                   'u_id': u_id,
                   'p_id': p_id,
                   'name': hi_name,
                   }

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Removing %s failed, Please try again." % manu.m_name,
                   'del_status': 0,
                   'u_id': u_id,
                   'p_id': p_id,
                   'name': hi_name,
                   }
    return render(request, 'user/products/delete.html', context)


def right_update(request, u_id=0, p_id=0, pm_id=0):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    update_pm = PMmapping.objects.get(id=pm_id)
    manu = Manufacturer.objects.get(m_id=update_pm.m_id)
    print(pm_id)
    context = {'u_id': u_id,
               'p_id': p_id,
               'pm_id': pm_id,
               'name': hi_name,
               'm_name': manu.m_name,
               }
    return render(request, 'user/products/right_change.html', context)


def right_updated(request, u_id=0, p_id=0, pm_id=0):
    update_pm = PMmapping.objects.get(id=pm_id)
    try:
        access_right = 0
        if request.POST.get("Read-only") is not None:
            access_right += int(request.POST.get("Read-only"))
        if request.POST.get("Write-only") is not None:
            access_right += int(request.POST.get("Write-only"))
        if request.POST.get("Distribute-only") is not None:
            access_right += int(request.POST.get("Distribute-only"))
        print(access_right, p_id, pm_id)
        update_pm.access_right = access_right
        update_pm.save()
    except Exception as err:
        print('***************')
        print(err)
    return redirect(reverse('mU_p_edit', kwargs={'u_id': u_id, 'p_id': p_id}))


def pm_recovery(request, u_id=0, p_id=0, pm_id=0):
    user_hi = User.objects.get(u_id=u_id)
    hi_name = user_hi.u_name.split('/')[0]
    rec_pm = PMmapping.objects.get(id=pm_id)
    manu = Manufacturer.objects.get(m_id=rec_pm.m_id)
    try:
        rec_pm.status = 0
        rec_pm.save()
        context = {'info': "Information recovery succeeded",
                   'add_status': 1,
                   'u_id': u_id,
                   'p_id': p_id,
                   'name': hi_name,
                   }

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Information recovery failed, Please try again.",
                   'add_status': 0,
                   'u_id': u_id,
                   'p_id': p_id,
                   'name': hi_name,
                   }
    return render(request, 'user/products/recovery.html', context)
