from dataclasses import dataclass, field
from .models import Order, CartItem, Cart, Address, ProductSimple

@dataclass
class OrderCore:
    user : object = field(default=None)
    shipping_address : object = field(default=None)
    order : object = field(init=False, default=None)
    cart : object = field(init=False, default = None)
    ip : str = field(default=None)

    def __post_init__(self):
        if not self.user: raise ValueError('User is required')
        self.shipping_address = self.validate_shipping_address()
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

    def validate_cart(self):
        if not Cart.objects.filter(user=self.user).exists():raise ValueError('Cart does not exist')
        return Cart.objects.get(user=self.user)
            

    def create_order(
        self,
        address_line_1 = None,
        address_line_2 = None,
        country = None,
        state = None,
        city = None,
        zip_code = None,
        name = None,
        phone = None,
        ):
        if not self.cart: raise ValueError('Cart does not exist')
        self.order = Order(
            user=self.user,
            shipping_address=self.shipping_address if self.shipping_address else self.create_shipping_address(country, state, city, address_line_1, address_line_2, zip_code , name, phone),
            ip = self.ip if self.ip else None,
        )

        self.order.save()
        
        for item in self.cart.items.all():
            self.order.items.add(item)
        
        self.order.save()
        return self.order

    def create_shipping_address(
        self,
        address_line_1 = None,
        address_line_2 = None,
        country = None,
        state = None,
        city = None,
        zip_code = None,
        name = None,
        phone = None,
        ):
        self.shipping_address = Address(
            country=country,
            state=state,
            city=city,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            zip_code=zip_code,
            name=name,
            phone=phone,
        )
        self.shipping_address.save()
        return self.shipping_address

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