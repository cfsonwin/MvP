from datetime import datetime

import folium
from django.shortcuts import render

from Admin.models import Product, CPmapping, User, PMmapping, Manufacturer
from Admin.utils import get_center_coor, Manus


# Create your views here.
def show_all(request, u_id):
    products = CPmapping.objects.filter(c_id=u_id)
    product_list = []
    for product in products:
        product_list.append(Product.objects.get(p_id=product.p_id))

    context = {'productlist': product_list,
               'u_id': u_id
               }
    return render(request, 'user/products/show.html', context)


def show_details(request, u_id, p_id=0):
    product = Product.objects.get(p_id=p_id)
    owners = CPmapping.objects.filter(p_id=p_id)
    manufacturers = PMmapping.objects.filter(p_id=p_id)
    products = CPmapping.objects.filter(c_id=u_id)
    p_id_list = []
    for p in products:
        p_id_list.append(p.p_id)
    P_list = Product.objects.filter(p_id__in=p_id_list).exclude(p_id=p_id)
    # for i in range(1, 10):
    #     try:
    #         print(Product.objects.get(p_id=i))
    #     except:
    #         print('no such record from id = %d' % i)
    #         break

    u_list = []
    try:
        for owner in owners:
            u_list.append(owner.c_id)
        loc_dic = {}
        m = folium.Map(width='100%', height='100%', location=get_center_coor(), zoom_start=8)
        for manufacturer in manufacturers:
            if manufacturer.m_pnode == 0:
                this_manu = Manufacturer.objects.get(m_id=manufacturer.m_id)
                loc_dic[manufacturer.id] = Manus(
                    this_manu.m_name,
                    this_manu.loc,
                    manufacturer.add_time,
                    manufacturer.modify_time,
                    manufacturer.modify_log,
                    "Direct get from product constructor"
                )
            elif manufacturer.m_pnode != 0:
                this_manu = Manufacturer.objects.get(m_id=manufacturer.m_id)
                loc_dic[manufacturer.id] = Manus(
                    this_manu.m_name,
                    this_manu.loc,
                    manufacturer.add_time,
                    manufacturer.modify_time,
                    manufacturer.modify_log,
                    "Get from %s" % Manufacturer.objects.get(m_id=manufacturer.m_pnode).m_name
                )
        for key in loc_dic.keys():
            info = loc_dic[key]
            html_1 = '''
            <head>
            <meta charset="utf-8">           
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
            </head>
            <body>
            <div class="card-body bg-light">
            <h4 class="card-text" style="margin-bottom:0px; font-size:18px">%s</h4>
            <p class="card-text" style="font-size:15px">Log:</br>%s</p>
            <p class="text-muted" style="font-size:15px; verticle-align:bottom">%s</p></div>
            </body>
            '''% (info.name, info.description, info.change_msg)
            iframe = folium.IFrame(html=html_1)
            popup = folium.Popup(iframe, min_width=400, max_width=400)
            folium.Marker([info.lat, info.lon], tooltip='click here for more',
                          popup=popup,
                          icon=folium.Icon(color='purple')).add_to(m)
        users = User.objects.filter(u_id__in=u_list)
        user_dic = {}
        for user in users:
            first_name = user.u_name.split('/')[0]
            family_name = user.u_name.split('/')[1]
            user_dic['%s %s' % (first_name, family_name)] = user.Email
        m_info = []
        m_html = m._repr_html_()
        context = {'loc_dic': loc_dic,
                   'u_id': u_id,
                   'user_dic': user_dic,
                   'map': m_html,
                   'add_status': 1,
                   'product': product,
                   'P_list': P_list
                   }

    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Showing information for product %s failed, Please try again." % product.p_name,
                   'add_status': 0}
    return render(request, 'user/products/view.html', context)


def edit(request, u_id, p_id=0):
    edit_product = Product.objects.get(p_id=p_id)
    # e_owners = CPmapping.objects.filter(p_id=p_id).exclude(c_id=u_id)
    e_owners = CPmapping.objects.filter(p_id=p_id)
    e_manufacturers = PMmapping.objects.filter(p_id=p_id)
    M_list = Manufacturer.objects.all()
    try:
        u_list = []
        manus_dic = {}
        for owner in e_owners:
            u_list.append(owner.c_id)
        for manufacturer in e_manufacturers:
            if manufacturer.m_pnode == 0:
                this_manu = Manufacturer.objects.get(m_id=manufacturer.m_id)
                manus_dic[manufacturer.id] = Manus(
                    this_manu.m_name,
                    this_manu.loc,
                    manufacturer.add_time,
                    manufacturer.modify_time,
                    manufacturer.modify_log,
                    'Get from Constructor directly'
                )
            elif manufacturer.m_pnode != 0:
                this_manu = Manufacturer.objects.get(m_id=manufacturer.m_id)
                manus_dic[manufacturer.id] = Manus(
                    this_manu.m_name,
                    this_manu.loc,
                    manufacturer.add_time,
                    manufacturer.modify_time,
                    manufacturer.modify_log,
                    'Get from %s.' % (Manufacturer.objects.get(m_id=manufacturer.m_pnode).m_name)
                )
        users = User.objects.filter(u_id__in=u_list)
        user_dic = {}
        for user in users:
            first_name = user.u_name.split('/')[0]
            family_name = user.u_name.split('/')[1]
            user_dic['%s %s' %(first_name, family_name)] = user.Email
        context = {'edit_product': edit_product,
                   'u_id': u_id,
                   'M_list': M_list,
                   'owners': users,
                   'manus_dic': manus_dic,
                   'user_dic': user_dic
                   }
        return render(request, 'user/products/edit.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later.",
                   'u_id': u_id,
                   }
        return render(request, 'user/products/info.html', context)


def updated(request, u_id, p_id):
    edit_product = Product.objects.get(p_id=p_id)
    try:
        edit_discription = request.POST['p_discription']
        edit_product.description = edit_discription
        edit_product.save()
        context = {'info': "description for Product %s has been successfully updated" % edit_product.p_name,
                   'update_status': 1,
                   'p_id': p_id,
                   'u_id': u_id,
                   }
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later.",
                   'update_status': 0,
                   'p_id': p_id,
                   'u_id': u_id,
                   }
    return render(request, 'user/products/update.html', context)
