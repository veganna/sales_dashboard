from dataclasses import dataclass, field
from .models import *

@dataclass
class OrderCore:
    user : object = field(default=None)
    shipping_address : object = field(default=None, init = False)
    billing_address : object = field(default=None, init = False)
    tax : object = field(default=None, init = False)
    coupon : object = field(default=None, init = False)
    order : object = field(init=False, default=None)
    cart : object = field(init=False, default = None)
    ip : str = field(default=None)

    def __post_init__(self):
        if not self.user: raise ValueError('User is required')
        self.shipping_address = self.validate_shipping_address()
        self.billing_address = self.validate_billing_address()
        self.cart = self.validate_cart()

    def validate_shipping_address(self):
        if self.shipping_address:
            return self.shipping_address
        elif self.order:
            if self.order.shipping_address:
                return self.order.shipping_address
            return None
        else:
            return None 

    def validate_billing_address(self):
        if self.billing_address:
            return self.billing_address
        elif self.order:
            if self.order.billing_address:
                return self.order.billing_address
            return None
        else:
            return None

    def validate_cart(self):
        if not Cart.objects.filter(user=self.user).exists():raise ValueError('Cart does not exist')
        return Cart.objects.get(user=self.user)
            

    def create_order(
        self,
        data
        ):
        if not self.cart: raise ValueError('Cart does not exist')
        self.order = Order(
            user=self.user,
            shipping_address=self.shipping_address if self.shipping_address else self.create_address(data, 'shipping_address'),
            billing_address=self.billing_address if self.billing_address else self.create_address(data, 'billing_address'),
            tax=self.tax if self.tax else self.get_tax(),
            coupon=self.coupon if self.coupon else self.validate_coupon(data),
        )

        self.order.save()
        
        for item in self.cart.items.all():
            self.order.items.add(item)
        
        self.order.save()
        return self.order

    def get_orders(self):
        return Order.objects.filter(user=self.user)

    def get_order(self, order_id):
        order = Order.objects.get(id=order_id)
        if order.user != self.user: raise ValueError('Order does not belong to user')
        return order

    def delete_order(self, order_id):
        order = Order.objects.get(id=order_id)
        if order.user != self.user: raise ValueError('Order does not belong to user')
        order.delete()
        return True

    def create_address(
        self,
        data,
        address_type
    ):
        if not data.get(f'{address_type}_address_line_1'): raise ValueError('Address line 1 is required')
        if not data.get(f'{address_type}_country'): raise ValueError('Country is required')
        if not data.get(f'{address_type}_state'): raise ValueError('State is required')
        if not data.get(f'{address_type}_city'): raise ValueError('City is required')
        if not data.get(f'{address_type}_zip_code'): raise ValueError('Zip code is required')
        address = Address(
            country=data.get(f'{address_type}_country'),
            state=data.get(f'{address_type}_state'),
            city=data.get(f'{address_type}_city'),
            address_line_1=data.get(f'{address_type}_address_line_1'),
            address_line_2=data.get(f'{address_type}_address_line_2'),
            zip_code=data.get(f'{address_type}_zip_code'),
            name=data.get(f'{address_type}_name'),
            phone=data.get(f'{address_type}_phone'),
        )
        
        address.save()
        if address_type == 'shipping_address':
            self.shipping_address = address
        elif address_type == 'billing_address':
            self.billing_address = address
            
        return address

    def get_tax(self):
        if not self.shipping_address: raise ValueError('Shipping address is required')
        state = self.shipping_address.state
        zip_code = self.shipping_address.zip_code

        tax = Tax.objects.filter(zip_code = zip_code).first()

        if not tax:
            tax = Tax.objects.filter(state = state).first()

        if not tax:
            return None

        return tax

    def validate_coupon(self, data):
        if not data.get('cupon_code'): return None
        coupon = Coupon.objects.filter(code=data.get('cupon_code')).first()
        if not coupon: raise ValueError('Coupon does not exist')
        if coupon.is_expired(): raise ValueError('Coupon is expired')
        if coupon.is_used(): raise ValueError('Coupon is used')
        if coupon.products.count() > 0:
            for item in self.cart.items.all():
                if item.product not in coupon.products.all():
                    raise ValueError('Coupon is not valid for this product')
        if self.user not in coupon.users.all(): raise ValueError('Coupon is not valid for user')
        return coupon