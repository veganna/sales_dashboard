from unicodedata import category
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
        products = [
            'T-shirt',
            'Shirt',
            'Pants',
            'Shorts',
            'Socks',
            'Shoes',
            'Hat',
            'Gloves',
            'Jacket',
            'Coat',
            'Sweater',
            'Dress',
            'Skirt',
            'Belt',
            'Scarf',
            'Underwear',
        ]

        names = [
            'alex',
            'james',
            'josh',
            'jake',
            'joe',
            'jason',
            'jordan',
            'joshua',
            'justin',
            'kyle',
            'kevin',
            'michael',
            'matthew',
            'mark',
            'matt',
            'nathan',
            'nick',
            'noah',
            'ryan',
            'robert',
            'sam',
            'scott',
            'sean',
            'steven',
            'tim',
        ]

        surnames = [
            'smith',
            'johnson',
            'williams',
            'brown',
            'jones',
        ]

        categories = [
            'Camel Style',
            'Casual',
            'Sport',
            'Man',
            'Woman',
            'Why Should We Choose',
            'Non Binary',
            'No Idea'
        ]

        addicional = [
            'Blue',
            'Green',
            'Yellow',
            'Classic',
            'Usual',
            'For Fat People Like Me'
        ]

        membership_names = [
            'Premium',
            'Basic',
            'Medium',
            'Free Shipping',
            'Member Plus'
        ]


        #create users
        for i in range(1, 100):
            user = User.objects.create_user(
                email="".join(random.choice(names)) + random.choice(surnames) + str(i) + "@fakemail.com",
                first_name="".join(random.choice(names)),
                last_name="".join(random.choice(surnames)),
                phone="".join(random.choice(string.digits) for _ in range(10)),
                password="".join(random.choice(string.ascii_letters) for _ in range(10)),
            )
            user.save()
            print("user"+str(i)+" created")

            _category = Category(
                name="".join(random.choice(categories) + " " + random.choice(addicional)),
            )
            _category.save()
            print("category"+str(i)+" created")

            product = ProductSimple(
                name="".join(random.choice(products) + " " + random.choice(addicional)),
                description="".join(random.choice(string.ascii_letters) for _ in range(100)),
                price=random.randint(1, 100),
                stock=random.randint(1, 100),
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
                    name="".join(random.choice(products) + " " + random.choice(addicional)),
                    description="".join(random.choice(string.ascii_letters) for _ in range(100)),
                    price=random.randint(1, 100),
                    stock=random.randint(1, 100),
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
                quantity=random.randint(1, 10),
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
                    billing_address=address,
                    ip=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)),
                    is_paid=True if i%2==0 else False,
                    is_shipped=True if i%4==0 else False,
                    is_delivered=True if i%10==0 else False,
                    is_completed=True if i%20==0 else False,
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
                    membership_name="".join(random.choice(membership_names)),
                    membership_price=random.randint(1, 100),
                    membership_lifetime=f"{random.randint(1, 5)} {random.choice(['day', 'week', 'month', 'year'])}",
                    membership_description="".join(random.choice(string.ascii_letters) for _ in range(100)),
                    is_abstract = True
                )
                membership_plan.save()

            if (i % 10) == 0:
                membership = Membership(
                    membership_user=user,
                    membership_name="".join(random.choice(membership_names)),
                    membership_price=random.randint(1, 100),
                    membership_lifetime=f"{random.randint(1, 5)} {random.choice(['day', 'week', 'month', 'year'])}",
                    membership_description="".join(random.choice(string.ascii_letters) for _ in range(100)),
                    is_abstract = False
                )
                membership.save()
                print("membership"+str(i)+" created")
            

            
            

            






