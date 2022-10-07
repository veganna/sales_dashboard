from django.core.management.base import BaseCommand
import string 
import random
from accounts.models import *
from ecommerce_simple.models import *
from django.core.files import File
from django.core.files.images import ImageFile



class Command(BaseCommand):
    help = 'Generate content'
    def handle(self, *args, **options):
        variable = []
        item_set = []
        #create users
        for i in range(1, 100):
            user = User.objects.create_user(
                email="user"+str(i)+"@example.com",
                first_name="user"+str(i),
                last_name="user"+str(i),
                phone="".join(random.choice(string.digits) for _ in range(10)),
                password="".join(random.choice(string.ascii_letters) for _ in range(10)),
            )
            user.save()
            print("user"+str(i)+" created")

            _category = Category(
                name="category"+str(i)
            )
            _category.save()
            print("category"+str(i)+" created")

            product = ProductSimple(
                name="product"+str(i),
                description="product"+str(i),
                price=10,
                stock=10,
                is_featured=True if i%2==0 else False,
                is_best_seller=True if i%20==0 else False,
                is_available=True,
                is_published=True,
            )
            product.save()
            product.category.add(_category)
            print("product"+str(i)+" created")
            
            variable.append(product)
            if (i % 5) == 0:
                product_variable = ProductVariable(
                    name="product_variable"+str(i),
                    description="product_variable"+str(i),
                    price=10,
                    stock=10,
                )
                product_variable.save()
                for j in range(5):
                    product_variable._product_variants.add(variable[j])
                    product_variable.save()

                product_variable.save()
                variable = []
                print("product_variable"+str(i)+" created")


            cart_item = CartItem(
                product=product,
                quantity=1,
            )
            cart_item.save()
            print("cart_item"+str(i)+" created")

            item_set.append(cart_item)
            if (i % 5) == 0:
                cart = Cart(
                    user=user,
                )
                cart.save()
                ip = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
                for j in range(5):
                    cart.items.add(item_set[j])
                    cart.save()
                item_set = []
                print("cart"+str(i)+" created")            

            if (i % 10) == 0:
                address = Address(
                    name = 'address'+str(i),
                    phone = ''.join(random.choice(string.digits) for _ in range(10)),
                    zip_code = ''.join(random.choice(string.digits) for _ in range(6)),
                    address_line_1 = 'address_line_1'+str(i),
                    address_line_2 = 'address_line_2'+str(i),
                    city = 'city'+str(i),
                    state = 'state'+str(i),
                    country = 'country'+str(i),
                )
                address.save()

                order = Order(
                    user=user,
                    shipping_address=address,
                    ip=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)),
                    is_paid=True,
                    is_shipped=True,
                    is_delivered=True,
                    is_completed=True,
                    tracking_number=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
                )
                order.save()
                for j in range(len(item_set)):
                    order.items.add(item_set[j])
                    order.save()
                
                print("order"+str(i)+" created")

            if (i % 20) == 0:
                membership_plan = Membership(
                    membership_user=user,
                    membership_name="membership"+str(i),
                    membership_price=10,
                    membership_lifetime=f"{i} month",
                    membership_description="membership"+str(i),
                    is_abstract = True
                )
                membership_plan.save()

            if (i % 10) == 0:
                membership = Membership(
                    membership_user=user,
                    membership_name="membership"+str(i),
                    membership_price=10,
                    membership_lifetime=f"{i} month",
                    membership_description="membership"+str(i),
                    is_abstract = False
                )
                membership.save()
                print("membership"+str(i)+" created")
            
            membership = Membership(
                membership_user=user,
                membership_name="membership"+str(i),
                membership_price=10,
                membership_lifetime=f"{i} month",
                membership_description="membership"+str(i),
                is_abstract = False
            )
            membership.save()

            
            

            






