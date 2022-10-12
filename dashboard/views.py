from accounts.models import User as costumer
from django.shortcuts import render
from django.views.generic import View
from .dashboardGeneric import *
from django.contrib.auth.hashers import make_password
# Create your views here.
from ecommerce_simple.models import *
from datetime import datetime, timedelta

# class GenerateGenericListView(View):
#     def get(self, request, model):
#         context = GenerateGenericList().build(model)
#         return render(request, 'dashboard/dashboard_generic_list.html', context)

#     def post(self, request, model):
#         filters = []
#         for key, value in request.POST.items():
#             if value != '' and key != 'csrfmiddlewaretoken' and key != 'submit':
#                 filters.append((key, value))
#         context = GenerateGenericList().build(model, filters)

#         return render(request, 'dashboard/dashboard_generic_list.html', context)

#     def options(self, request, model):
#         modelInstance = GenerateGenericList().get_model_by_name(model)
        

# class GenerateGenericDetailView(View):
#     def get(self, request, model, id):
#         context = GenerateGenericDetail().build(model, id)
#         return render(request, 'dashboard/dashboard_generic_detail.html', context)

#     def post(self, request, model, id):
#         fields = []
#         for key, value in request.POST.items():
#             if value != '' and key != 'csrfmiddlewaretoken' and key != 'submit':
#                 if key == 'password':
#                     value = make_password(value)
                
#                 if value == 'on':
#                     value = True
                
                
#                 #if there is a foreign key, we need to get the model reference
#                 if key.endswith('_id'):
#                     key = key.replace('_id', '')
#                     model = request.context[key]
#                     value = model.filter(id=value)

#                 #if it is a file field, we need to get the file
#                 if key.endswith('_file'):
#                     key = key.replace('_file', '')
#                     value = request.FILES[key]
#                     print("value",value)
                
#                 #id is a image field
#                 if key == 'image':
#                     print("value",value)
#                     value = request.FILES[key]

                
#                 print(key, value)
#                 fields.append((key, value))

#         context = GenerateGenericDetail().handler(model, id, fields)
#         return render(request, 'dashboard/dashboard_generic_detail.html', context)

# class GenerateGenericCreateView(View):
#     def get(self, request, model):
#         context = GenerateGenericDetail().build(model)
#         return render(request, 'dashboard/dashboard_generic_create.html', context)

#     def post(self, request, model):
#         fields = []
#         for key, value in request.POST.items():
#             model = None

#             if value != '' and key != 'csrfmiddlewaretoken' and key != 'submit':
#                 if key == 'password':
#                     value = make_password(value)
                
#                 if value == 'on':
#                     value = True
                
                
#                 #if there is a foreign key, we need to get the model reference
#                 if key.endswith('_id'):
#                     key = key.replace('_id', '')
#                     model = request.context[key]
#                     value = model.filter(id=value)

#                 #if it is a file field, we need to get the file
#                 if key.endswith('_file'):
#                     key = key.replace('_file', '')
#                     value = request.FILES[key]
#                     print("value",value)
                
#                 #id is a image field
#                 if key == 'image':
#                     value = request.FILES[key]
#                     print("value",value)

                
#                 print(key, value)

#                 fields.append((key, value))

#         context = GenerateGenericDetail().handler(model, fields)
#         return render(request, 'dashboard/dashboard_generic_create.html', context)


# class GenerateGenericDeleteView(View):
#     def post(self, request, model, id):
#         GenerateGenericDetail().delete(model, id)
#         context = GenerateGenericList().build(model, id)
#         return render(request, 'dashboard/dashboard_generic_list.html', context)

class DashboardPage(View):
    def get(self, request):
        orders = Order.objects.filter(is_paid=True)

        # filter by last month
        last_month = datetime.now() - timedelta(days=30)
        orders_last_month = orders.filter(created_at__gte=last_month)
        #filter by previous month
        previous_month = datetime.now() - timedelta(days=60)
        orders_previous_month = orders.filter(created_at__gte=previous_month, created_at__lte=last_month)

        # calculate the change between last month and previous month
        orders_last_month_count = orders_last_month.count()
        orders_previous_month_count = orders_previous_month.count()
        orders_change = orders_last_month_count - orders_previous_month_count
        if orders_previous_month_count != 0:
            orders_change_percentage = orders_change / orders_previous_month_count * 100
        else:
            if orders_last_month_count > 0:
                orders_change_percentage = 100
            else:
                orders_change_percentage = 0

        total = 0
        for order in orders:
            total += order.get_total()
        average = total / len(orders)
        # 2 decimal places
        average = round(average, 2)
        context = {
            'orders': len(orders),
            'orders_change': orders_change_percentage,
            'total': total,
            'average': average
        }
        print(orders, total, average)

        return render(request, 'dashpages/admin/overview.html', context)

class ProductOverviewPage(View):
    def get(self, request):
        return render(request, 'dashpages/products/products.html')




class EditProductSimple(View):
    def get(self, request):
        return render(request, 'dashpages/products/edit-product-simple.html')

class EditProductVariable(View):
    def get(self, request):
        return render(request, 'dashpages/products/edit-product-variable.html')

class EditProductDigital(View):
    def get(self, request):
        return render(request, 'dashpages/products/edit-product-digital.html')

class AdminSettings(View):
    def get(self, request):
        return render(request, 'dashpages/admin/settings.html')
class AdminLogin(View):
    def get(self, request):
        return render(request, 'dashpages/admin/login.html')
class Customers(View):
    def get(self, request):
        return render(request, 'dashpages/customers/customers.html')
class CustomerDetail(View):
    def get(self, request):
        return render(request, 'dashpages/customers/customer-detail.html')
class Orders(View):
    def get(self, request):
        return render(request, 'dashpages/orders/orders.html')
class OrderDetail(View):
    def get(self, request):
        return render(request, 'dashpages/orders/order-detail.html')
class Subscriptions(View):
    def get(self, request):
        return render(request, 'dashpages/subscriptions/subscriptions.html')
class SubscriptionDetail(View):
    def get(self, request):
        return render(request, 'dashpages/subscriptions/subscription-detail.html')
class SubscriberDetail(View):
    def get(self, request):
        return render(request, 'dashpages/subscriptions/subscriber-detail.html')
class Subscribers(View):
    def get(self, request):
        return render(request, 'dashpages/subscriptions/subscribers.html')
