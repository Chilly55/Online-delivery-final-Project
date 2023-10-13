from django.shortcuts import render

# Create your views here.
from django.views import View
from.models import MenuItem, Category, OrderModel

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')
    
class Order(View):
    def get(self, request, *args, **kwargs):
        
        breakfasts = MenuItem.objects.filter(category__name__contains='Breakfast')
        burgers = MenuItem.objects.filter(category__name__contains='Burger')
        sides = MenuItem.objects.filter(category__name__contains='Side')
        beverages = MenuItem.objects.filter(category__name__contains='Beverage')

        context = {
            'breakfasts': breakfasts,
            'burgers': burgers,
            'sides': sides,
            'beverages': beverages,
        }

        return render(request, 'customer/order.html', context)
    
    def post(self, request, *args, **kwards):
        order_items = {
            'items':[]
        }
        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)


            price = 0     #total price of order
            item_ids = []

        for item in order_items['items']:
            item_ids.append(item['id'])
            price += item['price'] #adds items price to the total

        order = OrderModel.objects.create(price=price)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }
        return render(request, 'customer/order_conformation.html', context)