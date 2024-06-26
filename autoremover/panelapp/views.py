from django.shortcuts import render, redirect
from .decorators import login_required, staff_required, admin_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from database.models import *

import requests
import json

# Create your views here.

def login_page(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/panel/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.POST.get('next'):
            redirect_url = request.POST.get('next')
        else:
            redirect_url = "/panel/"

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redirect_url)

        else:
            messages.error(request, "Invalid username or password!")
            if redirect_url != "/panel/":
                return redirect(reverse('Panel Login') + f'?next={redirect_url}')


    context = {
        'page_title': 'Panel Login',
        'styling_files': [],
        'script_files': [],
        }
    
    return render(request, "panelapp/pages/panel_login.html", context)

@login_required
@staff_required
def logout_view(request):
    logout(request)
    return redirect('Panel Login')

@login_required
@staff_required
def file_requests_page(request):

    context = {
        'page_title': 'File Requests',
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'script_files': ["file_requests.js"],
        'is_panel_app': True,
        }
    
    return render(request, 'panelapp/pages/file_requests.html', context)

@login_required
@staff_required
def file_requests_modal(request):
    params = request.GET
    page_param = params.get('page')

    req_list = FileRequest.objects.order_by("-created_at", "-status")

    if page_param:
        pagenum = int(page_param)
    else:
        pagenum = 1

    paginator = Paginator(req_list, 10)
    page = paginator.page(int(pagenum))
    start_page = max(1, page.number - 5)
    end_page = min(paginator.num_pages, max(page.number + 5, 10))
    page_list = range(start_page, end_page + 1)

    ip = SystemSetting.objects.all()[0].vehicle_data_backend_ip
    port = SystemSetting.objects.all()[0].vehicle_data_backend_port
    url = f"http://{ip}:{port}/api/vehicle_data/"

    payload = {'requests': json.dumps(['vehicle']), 'vehicle_filters': json.dumps({"ids": list(set([d.vehicle for d in page.object_list]))})}
    response = requests.get(url, params=payload)
    vehicle_data = response.json().get("data").get("vehicle").get("data")

    reqs_data = []
    for f in page.object_list:
        vehicle = [d for d in vehicle_data if d.get("id") == f.vehicle][0]
        file = {
            'id': f.id,
            'status_long': f.status_long,
            'vehicle': {'vehicle_long': vehicle["vehicle_brand"] + " " + vehicle["vehicle_model"] + " " + str(vehicle["vehicle_year"]), 'vehicle_version': vehicle["vehicle_version"], 'ecu_model': vehicle["ecu_model"]},
            'processes_string': f.processes_string,
            'created_at': f.created_at,
            'customer': f.customer,
            'employee': f.employee,
        }
        reqs_data.append(file)

    context = {
        'data_amount': paginator.count,
        'start_index': page.start_index(),
        'end_index': page.end_index(),
        'current_page': page.number,
        'previous_page_disabled': not page.has_previous(),
        'following_page_disabled': not page.has_next(),
        'page_list': page_list,
        'file_requests': reqs_data
        }
    
    return render(request, 'panelapp/modals/file_request_modal.html', context)

@login_required
@admin_required
def pricing_page(request):
    ip = SystemSetting.objects.all()[0].vehicle_data_backend_ip
    port = SystemSetting.objects.all()[0].vehicle_data_backend_port
    url = f"http://{ip}:{port}/api/vehicle_data/"

    payload = {'requests': json.dumps(['vehicle_category', 'ecu_type', 'vehicle']), 'ecu_type_keyword': ' ', 'vehicle_filters': json.dumps({}), 'vehicle_page': 1}
    response = requests.get(url, params=payload)
    
    category_data = json.loads(response.json().get("data").get("vehicle_category"))
    vehicle_categories = [{'id': d['pk'], 'name': d['fields']['name']} for d in category_data]
    ecu_pagination = response.json().get("data").get("ecu_pagination")
    ecu_types = response.json().get("data").get("ecu_type")
    vehicle_data = response.json().get("data").get("vehicle")

    context = {
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'page_title': 'Process Pricing',
        'vehicle_category_list': vehicle_categories,
        'script_files': ["pricing_page.js"],
        'is_panel_app': True,
        'data_amount': ecu_pagination.get("data_amount"),
        'start_index': ecu_pagination.get("start_index"),
        'end_index': ecu_pagination.get("end_index"),
        'current_page': ecu_pagination.get("current_page"),
        'previous_page_disabled': ecu_pagination.get("previous_page_disabled"),
        'following_page_disabled': ecu_pagination.get("following_page_disabled"),
        'page_list': ecu_pagination.get("page_list"),
        'ecu_types': ecu_types,
        'vehicle_data': vehicle_data,
        'processes': FileProcess.objects.all().order_by('name'),
        }
    return render(request, 'panelapp/pages/pricing.html', context)

@login_required
@admin_required
def ecu_type_search_modal(request):
    ip = SystemSetting.objects.all()[0].vehicle_data_backend_ip
    port = SystemSetting.objects.all()[0].vehicle_data_backend_port
    url = f"http://{ip}:{port}/api/vehicle_data/"

    keyword = request.GET.get('ecu_type_keyword')
    page = request.GET.get('ecu_type_page')
    if page is None:
        page = 1

    payload = {'requests': json.dumps(['ecu_type']), 'ecu_type_keyword': keyword, 'ecu_type_page': page}
    response = requests.get(url, params=payload)
    ecu_pagination = response.json().get("data").get("ecu_pagination")
    ecu_types = response.json().get("data").get("ecu_type")

    context = {
        'data_amount': ecu_pagination.get("data_amount"),
        'start_index': ecu_pagination.get("start_index"),
        'end_index': ecu_pagination.get("end_index"),
        'current_page': ecu_pagination.get("current_page"),
        'previous_page_disabled': ecu_pagination.get("previous_page_disabled"),
        'following_page_disabled': ecu_pagination.get("following_page_disabled"),
        'page_list': ecu_pagination.get("page_list"),
        'ecu_types': ecu_types
    }
    return render(request, 'panelapp/modals/ecu_type_modal.html', context)

@login_required
@admin_required
def filter_vehicles_modal(request):
    ip = SystemSetting.objects.all()[0].vehicle_data_backend_ip
    port = SystemSetting.objects.all()[0].vehicle_data_backend_port
    url = f"http://{ip}:{port}/api/vehicle_data/"

    params = request.GET
    filters = params.get('vehicle_filters')
    page = params.get('vehicle_page')

    payload = {'requests': json.dumps(['vehicle']), 'vehicle_filters': filters, 'vehicle_page': page}
    response = requests.get(url, params=payload)
    data = response.json().get("data").get("vehicle")

    context = {
        'vehicle_data': data
    }
    return render(request, 'panelapp/modals/vehicle_filter_modal.html', context)

@login_required
@admin_required
def make_pricing_modal(request):
    params = request.POST
    
    version_ids = params.getlist('version_filter')
    ecu_type_ids = params.getlist('ecu_filter')
    filters = {"vehicle_versions": version_ids, "ecu_models": ecu_type_ids}
    
    ip = SystemSetting.objects.all()[0].vehicle_data_backend_ip
    port = SystemSetting.objects.all()[0].vehicle_data_backend_port
    url = f"http://{ip}:{port}/api/vehicle_data/"

    payload = {'requests': json.dumps(['vehicle']), 'vehicle_filters': json.dumps(filters)}
    response = requests.get(url, params=payload)
    vehicles = response.json().get("data").get("vehicle").get("data")

    pricings = {}
    
    for key, value in params.items():
        if key.startswith('slave') or key.startswith('master'):
            if len(value) > 0:
                first_underscore = key.find('_')
                last_underscore = key.rfind('_')
                tool_type = key[:first_underscore]
                process_id = int(key[last_underscore+1:])
                currency = key[first_underscore+1:last_underscore]
                price = int(value)
                if pricings.get(process_id) is None:
                    pricings[process_id] = {}
                
                pricings[process_id][f"{tool_type}_{currency}_price"] = price

    cleared_pricings = [int(id) for id in params.getlist("cancel_pricings")]
    ProcessPricing.objects.filter(id__in=cleared_pricings).update(master_try_price=None, master_eur_price=None, slave_try_price=None, slave_eur_price=None)
    
    for vehicle in vehicles:
        vehicle_id = int(vehicle["id"])
        for process_id, pricing in pricings.items():
            obj, created = ProcessPricing.objects.update_or_create(vehicle=vehicle_id, process_id=process_id, defaults=pricing)

    messages.success(request, "Pricing has been performed successfully!")
    return redirect('Panel Pricing')

@login_required
@admin_required
def customer_options(request):
    if request.method == "POST":
        if request.POST.get('form_name') == "add_process":
            process_name = request.POST.get('process_name')
            try:
                process = FileProcess.objects.create(name=process_name)
                messages.success(request, f"File process '{process.name}' has been added successfully!")
            except:
                messages.error(request, "File process could not be saved!")

        elif request.POST.get('form_name') == "update_process":
            process_id = int(request.POST.get('process_id'))
            process_name = request.POST.get('process_name')
            try:
                process = FileProcess.objects.get(id=process_id)
                old_name = process.name
                process.name = process_name
                process.save()
                messages.success(request, f"File process '{old_name}' has been updated as '{process.name}' successfully!")
            except:
                messages.error(request, "File process could not be updated!")
        
        elif request.POST.get('form_name') == "add_tool":
            tool_name = request.POST.get('tool_name')
            try:
                tool = ConnectionTool.objects.create(name=tool_name)
                messages.success(request, f"Connection tool '{tool.name}' has been added successfully!")
            except:
                messages.error(request, "Connection tool could not be saved!")

        elif request.POST.get('form_name') == "update_tool":
            tool_id = int(request.POST.get('tool_id'))
            tool_name = request.POST.get('tool_name')
            try:
                tool = ConnectionTool.objects.get(id=tool_id)
                old_name = tool.name
                tool.name = tool_name
                tool.save()
                messages.success(request, f"Connection tool '{old_name}' has been updated as '{tool.name}' successfully!")
            except:
                messages.error(request, "Connection tool could not be updated!")

        return redirect('Panel Customer Options')

    context = {
        'page_title': 'Customer Options',
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'processes': FileProcess.objects.all().order_by('name'),
        'tools': ConnectionTool.objects.all().order_by('name'),
    }
    return render(request, 'panelapp/pages/customer_options.html', context)

@login_required
@admin_required
def customers_page(request):
    context = {
        'page_title': 'Manage Customers',
        'file_service_status': 'ONLINE',
        'file_service_until': datetime.now(),
        'customers': Customer.objects.all().order_by('user__first_name'),
    }
    return render(request, 'panelapp/pages/customers.html', context)

@login_required
@admin_required
def update_customer(request):
    params = request.POST

    customer_id = params.get("customer_id")
    credit_addition_amount = params.get("credit_addition_amount")
    pricing_class = params.get("pricing_class")
    is_banned = params.get("is_banned")

    customer = Customer.objects.get(id=customer_id)

    if pricing_class != customer.pricing_class:
        customer.pricing_class = pricing_class

    customer.user.is_active = not is_banned
    customer.user.save()
    customer.save()

    if credit_addition_amount:
        credit_amount = int(credit_addition_amount)
        transaction = Transaction.objects.create(customer=customer, amount=credit_amount)

    messages.success(request,f"Customer {str(customer)} updated successfully!")

    return redirect("Panel Manage Customers")

