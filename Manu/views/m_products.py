from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse

from Admin.models import Product, PMmapping, Manufacturer


# Create your views here.
def select_a_product(request, m_id):
    p_id_list = []
    owned_p = PMmapping.objects.filter(m_id=m_id)
    for p in owned_p:
        p_id_list.append(p.p_id)
    products = Product.objects.filter(p_status=1).exclude(p_id__in=p_id_list)
    context = {
        'm_id': m_id,
        'products': products,
    }
    return render(request, 'manu/products/select_p.html', context)


def warning(request, m_id):
    context = {
        "info": "Please don't add again!",
        "m_id": m_id,
    }
    return render(request, 'manu/products/info.html', context)


def select_a_pnode(request, m_id):
    try:
        if request.POST["mM_pnode_select"] == "select_by_name":
            p_id = request.POST['p_selected']
        elif request.POST["mM_pnode_select"] == "select_by_searchID":
            search_id = request.POST["p_search_id"]
            product = Product.objects.get(search_id=search_id)
            p_id = product.p_id
            this_p_pm_record = PMmapping.objects.filter(p_id=p_id)
            for pm_record in this_p_pm_record:
                if int(pm_record.m_id) == int(m_id):
                    return redirect(reverse('mM_warning', kwargs={'m_id': m_id}))
        pnode_list = []
        pnodes = PMmapping.objects.filter(p_id=p_id)
        for p in pnodes:
            pnode_list.append(p.m_id)
        Manus = Manufacturer.objects.filter(m_id__in=pnode_list)
        context = {
            'manus': Manus,
            'm_id': m_id,
            'p_id': p_id,
        }

        return render(request, 'manu/products/select_pnode.html', context)
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Search ID not exist, Try again later",
                   'm_id': m_id,
                   }
        return render(request, 'manu/products/info.html', context)




def add_pmmapping(request, m_id, p_id):
    try:
        selected_pnode = int(request.POST['pnode_selected'])
        new_pmmapping = PMmapping()
        if selected_pnode == 0:
            pnode_level = 0
        else:
            pnode_record = PMmapping.objects.filter(p_id=p_id).get(m_id=selected_pnode)
            pnode_level = pnode_record.m_Tlevel
        new_pmmapping.p_id = p_id
        new_pmmapping.m_id = m_id
        new_pmmapping.m_pnode = selected_pnode
        new_pmmapping.m_Tlevel = int(pnode_level) + 1
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_pmmapping.modify_log = "%s::First time added;;;" % time_now
        new_pmmapping.add_time = time_now
        new_pmmapping.modify_time = time_now
        new_pmmapping.status = 2
        new_pmmapping.feedback = 'No feedback'
        new_pmmapping.producing_period = 'No record'
        new_pmmapping.save()
        return redirect(reverse('mM_index', kwargs={'m_id': m_id}))
    except Exception as err:
        print('***************')
        print(err)
        context = {'info': "Unknown Error occurred, Please try again later.",
                   'm_id': m_id,
                   }
        return render(request, 'manu/products/info.html', context)


def view(request, m_id, p_id):
    products = PMmapping.objects.filter(m_id=m_id).exclude(p_id=p_id)
    pm_record = PMmapping.objects.filter(m_id=m_id).get(p_id=p_id)
    log = pm_record.modify_log
    i = 0
    log_dic = {}
    while log.split(';;;')[i] != '':
        log_dic[log.split(';;;')[i].split('::')[0]] = log.split(';;;')[i].split('::')[1]
        i += 1
    product = Product.objects.get(p_id=p_id)
    productlist_valid = []
    for p in products:
        if int(p.status) == 0 or int(p.status) == 4:
            _product = Product.objects.get(p_id=p.p_id)
            productlist_valid.append(_product)
    context = {'product': product,
               'productlist_valid': productlist_valid,
               'pm_record': pm_record,
               'm_id': m_id,
               'p_id': p_id,
               'log_dic': log_dic,
               }
    return render(request, 'manu/products/view.html', context)


def jump_to(request, m_id):
    p_id = request.POST['p_id_selected']
    return redirect(reverse('mM_view', kwargs={'m_id': m_id, 'p_id': p_id}))


def add_log(request, m_id, p_id):
    pm_record = PMmapping.objects.filter(m_id=m_id).get(p_id=p_id)
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    old_log = pm_record.modify_log
    log = request.POST.get('new_log')
    new_log = old_log + "%s::%s;;;" % (time_now, log)
    pm_record.modify_log = new_log
    pm_record.modify_time = time_now
    pm_record.save()
    return redirect(reverse('mM_view', kwargs={'m_id': m_id, 'p_id': p_id}))


def addProducingPeriod(request, m_id, p_id):
    pm_record = PMmapping.objects.filter(m_id=m_id).get(p_id=p_id)
    pm_record.producing_period = request.POST.get('new_ProducingPeriod')
    pm_record.save()
    return redirect(reverse('mM_view', kwargs={'m_id': m_id, 'p_id': p_id}))


def mStatusUpdate(request, m_id, p_id):
    pm_record = PMmapping.objects.filter(m_id=m_id).get(p_id=p_id)
    pm_record.m_status = request.POST.get('update_status')
    pm_record.save()
    return redirect(reverse('mM_view', kwargs={'m_id': m_id, 'p_id': p_id}))

def feedback(request, m_id, p_id):
    pm_record = PMmapping.objects.filter(m_id=m_id).get(p_id=p_id)
    feedback = pm_record.feedback
    print(feedback)
    if feedback == "No feedback":
        context = {'status': 0,
                   'm_id': m_id,
                   'p_id': p_id,
                   }
    else:
        if pm_record.status == 4:
            feedback_dic = {}
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
        print(feedback_dic)
        context = {'feedback_dic': feedback_dic,
                   'm_id': m_id,
                   'p_id': p_id,
                   'status': status_feedback,
                   }
    return render(request, 'manu/products/feedback.html', context)


def insert_feedback(request, m_id, p_id):
    pm_record = PMmapping.objects.filter(m_id=m_id).get(p_id=p_id)
    old_feedback = pm_record.feedback
    if old_feedback == "No feedback":
        new_feedback = '%s::' % request.POST.get('new_feedback')
    else:
        new_feedback = old_feedback + '%s::' % request.POST.get('new_feedback')
    pm_record.feedback = new_feedback
    pm_record.status = 4
    pm_record.save()
    return redirect(reverse('mM_feedback', kwargs={'m_id': m_id, 'p_id': p_id}))
