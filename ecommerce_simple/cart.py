from .models import *
from dataclasses import dataclass

@dataclass
class CartCore:
    user : object
    ip : str = None
    
    def __post_init__(self):
        self.user = self.user
        self.ip = self.ip

    def get_cart(self):
        if self.user:
            if Cart.objects.filter(user=self.user).exists():
                self.cart = Cart.objects.get(user=self.user)
                return self.cart
            else:
                self.cart = Cart(
                    user=self.user,
                    ip=self.ip if self.ip else "0.0.0.0"
                    )
                self.cart.save()
                return self.cart
                

    def add_to_cart(self, product_id, quantity):
        if self.user:
            self.cart = self.get_cart()
            if not self.cart:
                self.cart = Cart(
                    user=self.user,
                    ip=self.ip if self.ip else "0.0.0.0"
                )
            product = ProductSimple.objects.get(id=product_id)
            if product:
                cart_item = self.cart.items.filter(product=product)
                if cart_item:
                    cart_item[0].quantity += quantity
                    cart_item[0].save()  
                    return self.cart
                
                item = CartItem(
                    product=product,
                    quantity=quantity,
                )
                item.save()
                self.cart.items.add(item)
                self.cart.save()
                return self.cart
            else:
                raise Exception("Product not found")
        else:
            raise Exception("User not found")

    

    def remove_from_cart(self, product_id, quantity):
        if not self.user:
            raise Exception("User not found")
        self.cart = self.get_cart()
        
        if not self.cart:
            raise Exception("Cart not found")
        product = ProductSimple.objects.filter(id=product_id)
        
        if not product:
            raise Exception("Product not found")
        
        cart_item = self.cart.items.filter(product=product[0])
        
        if not cart_item:
            raise Exception("Cart Item not found")

        validator = cart_item[0].quantity - quantity
        
        if validator <= 0:
            cart_item[0].delete()
            return self.cart

        cart_item[0].quantity -= quantity
        cart_item[0].save()

        return self.cart


    def get_cart_items(self):
        if not self.user:
            raise Exception("User not found")
        self.cart = self.get_cart()
        if not self.cart:
            raise Exception("Cart not found")
        return self.cart.items.all()

    def get_cart_total(self):
        if not self.user:
            raise Exception("User not found")
        self.cart = self.get_cart()
        if not self.cart:
            raise Exception("Cart not found")
        total = 0
        for item in self.cart.items.all():
            total += item.product.price * item.quantity
        return total

    def get_cart_total_items(self):
        if not self.user:
            raise Exception("User not found")
        self.cart = self.get_cart()
        if not self.cart:
            raise Exception("Cart not found")
        total = 0
        for item in self.cart.items.all():
            total += item.quantity
        return total

    def delete_cart(self):
        if not self.user:
            raise Exception("User not found")
        self.cart = self.get_cart()
        if not self.cart:
            raise Exception("Cart not found")
        self.cart.delete()
        return True

            
