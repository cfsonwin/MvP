from django.shortcuts import render

from Admin.models import Product, CPmapping, User, PMmapping, Manufacturer
from Admin.utils import get_center_coor, Manus, LineInfo

# Create your views here.
from User.utils import get_centroid


def show_all(request):
    product = Product.objects
    p_list = product.all()
    context = {'productlist': p_list}
    return render(request, 'admin/products/show.html', context)


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


def show_details_2(request, p_id=0):
    product = Product.objects.get(p_id=p_id)
    owners = CPmapping.objects.filter(p_id=p_id)
    valid_status = [0, 4]
    need_valid_status = [2]
    no_valid_status = [1]
    manufacturers_valid = PMmapping.objects.filter(p_id=p_id).filter(status__in=valid_status)
    manufacturers_need_valid = PMmapping.objects.filter(p_id=p_id).filter(status__in=need_valid_status)
    manufacturers_no_valid = PMmapping.objects.filter(p_id=p_id).filter(status__in=no_valid_status)
    manufacturers = PMmapping.objects.filter(p_id=p_id)
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
                   'p_id': p_id,
                   'user_dic': user_dic,
                   'lat': lat,
                   'lon': lon,
                   'line_dic': line_dic,
                   'zoom_index': zoom_index,
                   'add_status': 1,
                   'product': product,
                   'line_dic_need_valid': line_dic_need_valid,
                   'loc_dic_need_valid': loc_dic_need_valid,
                   'line_dic_no_valid': line_dic_no_valid,
                   'loc_dic_no_valid': loc_dic_no_valid,
                   }

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Showing information for product %s failed, Please try again." % product.p_name,
                   'p_id': p_id,
                   'add_status': 0,
                   }
    return render(request, 'admin/products/view.html', context)


def edit(request, p_id=0):
    edit_product = Product.objects.get(p_id=p_id)
    try:
        context = {'edit_product': edit_product,
                   }
        return render(request, 'admin/products/edit.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later."}
        return render(request, 'admin/products/info.html', context)


def updated(request, p_id):
    edit_product = Product.objects.get(p_id=p_id)
    try:
        edit_discription = request.POST['p_discription']
        edit_product.description = edit_discription
        edit_product.save()
        context = {'info': "description for Product %s has been successfully updated" % edit_product.p_name,
                   'update_status': 1,
                   'p_id': p_id
                   }
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later.",
                   'update_status': 0,
                   'p_id': p_id
                   }
    return render(request, 'admin/products/update.html', context)
