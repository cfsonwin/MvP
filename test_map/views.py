from django.shortcuts import render
from geopy.geocoders import Nominatim

from Admin.models import Product, CPmapping, User, PMmapping
import numpy as np



# Create your views here.

def index(request):
    map_loc = [51.505, -0.09]
    test = '123'
    popup_html = '''
    <html>
    <head>
        <style type="text/css" abt="234"></style>
    </head>
    <body style="background-color:powderblue">
    <h1>{{ test }}</h1>
    </body>
    </html>'''
    context = {
        'map_loc': map_loc,
        'test': test,
        'popup_html': popup_html
    }
    return render(request, 'test/index.html', context)


def iframe(request, uid=0):
    test = request.POST['add_method_selected']
    context = {
        'test': test,
    }
    return render(request, 'test/iframe.html', context)


def select_test(request):
    context = {
        'test': 'test',
    }
    return render(request, 'test/select.html', context)


def get_select_info(request):
    selected_method = request.POST['select_method']
    if selected_method == "AddManually":
        info = "Add Manually"
        addr = '%s, %s, %s, %s' % (
            request.POST['Address'],
            request.POST['City'],
            request.POST['Zip'],
            request.POST['State']
        )

    elif selected_method == "SelectFromMap":
        geolocator = Nominatim(user_agent="get_location")
        latitude = request.POST['lat_fm']
        longitude = request.POST['lon_fm']
        location = geolocator.reverse((latitude, longitude))
        info = "Select From Map\n"
        addr = location.address
    else:
        info = "error"
        addr = ""
    print(info)
    context = {
        'info': info,
        'addr': addr,
    }
    return render(request, 'test/select_info.html', context)


def chart_generate(request):
    user = User.objects.get(u_id=7)
    products = CPmapping.objects.filter(c_id=7)
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
                    print(key, sum_dict[key])
                    sum_dict[key] += 1

    print(sum_dict)
    print(user, pid_list, m_list, chart_1_info, add_year_list)
    context = {
        'test': 'test',
        'info': chart_1_info,
        'p_list': p_name_list,
        'info2': sum_dict
    }
    return render(request, 'test/chart.html', context)
