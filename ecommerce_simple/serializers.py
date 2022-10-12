from inflection import tableize
from requests import request
from rest_framework import serializers
from .models import *
from accounts.models import BaseUserManager, User

class UserESerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'description')


class ProductSimpleSerializer(serializers.ModelSerializer):
    gallery = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = ProductSimple
        fields = ['name', 'description', 'price', 'image', 'categories', 'stock', 'id', 'gallery']

    def get_gallery(self, obj):
        return GallerySerializer(obj.gallery, many=False).data 

    def get_categories(self, obj):
        return CategorySerializer(obj.category.all(), many=True).data

        
class ProductVariableSerializer(serializers.ModelSerializer):
    variations = serializers.SerializerMethodField()

    def get_variations(self, obj):
        try:
            return ProductSimpleSerializer(obj._product_variants.all(), many=True).data
        except:
            return []

    class Meta:
        model = ProductVariable
        fields = ['id', 'name', 'description', 'price', 'image', 'stock', 'variations']
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class GetAllProductsSerializer(serializers.Serializer):
    simple = ProductSimpleSerializer(many=True)
    variable = ProductVariableSerializer(many=True)

class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = ['name', 'image', 'alt_tag']

class GallerySerializer(serializers.ModelSerializer):
    gallery_items = serializers.SerializerMethodField()

    def get_gallery_items(self, obj):
        try:
            return GalleryItemSerializer(obj.items.all(), many=True).data
        except:
            return []

    class Meta:
        model = Gallery
        fields = ['name', 'gallery_items']

    

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def get_product(self, obj):
        try:
            return ProductSimpleSerializer(obj.product, many=False).data
        except:
            return []

class CartSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('cart', 'total_price', 'total_items')

    def get_cart(self, obj):
        try:
            return CartItemSerializer(obj.items.all(), many=True).data
        except:
            return "No items in cart"

    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return total

    def get_total_items(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.quantity
        return total

    

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class CartItemResponseSerializer(serializers.Serializer):
    product = ProductSimpleSerializer(many=False)
    quantity = serializers.IntegerField()

class CartResponseSerializer(serializers.Serializer):
    cart = CartItemResponseSerializer(many=True)
    total_cost = serializers.IntegerField()
    total_items = serializers.IntegerField()

    class Meta:
        fields = ['cart', 'total_cost', 'total_items']



class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    billing_address = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'tax', 'coupon','is_paid', 'total_items', 'is_shipped', 'is_delivered',  'is_completed', 'tracking_number', 'shipping_address', 'billing_address','created_at', 'updated_at', 'coupon']

    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return total

    def get_total_items(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.quantity
        return total

    def get_user(self, obj):
        return UserESerializer(obj.user, many=False).data

    def get_items(self, obj):
        return CartItemSerializer(obj.items.all(), many=True).data

    def get_shipping_address(self, obj):
        try:
            return AddressSerializer(obj.shipping_address, many=False).data
        except:
            return []

    def get_billing_address(self, obj):
        try:
            return AddressSerializer(obj.billing_address, many=False).data
        except:
            return []

    def get_tax(self, obj):
        try:
            return TaxSerializer(obj.tax, many=False).data
        except:
            return []

    def get_coupon(self, obj):
        try:
            return CouponSerializer(obj.coupon, many=False).data
        except:
            return []
    

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_line_1', 'address_line_1', 'city', 'phone', 'name' ,'country', 'zip_code']

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['id', 'zip_code', 'state', 'tax_rate']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'type', 'amount']

class OrderResponseSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserESerializer(many=False)
    shipping_address = AddressSerializer(many=False)
    billing_address = AddressSerializer(many=False)
    items = CartItemResponseSerializer(many=True)
    is_paid = serializers.BooleanField()
    is_shipped = serializers.BooleanField()
    is_delivered = serializers.BooleanField()
    is_completed = serializers.BooleanField()
    total_cost = serializers.IntegerField()
    total_items = serializers.IntegerField()
    coupon = CouponSerializer(many=False)
    tax = TaxSerializer(many=False)

class CreateOrderSerializer(serializers.Serializer):
    billing_address_address_line_1 = serializers.CharField(required = True)
    billing_address_address_line_2 = serializers.CharField(required = False)
    billing_address_state = serializers.CharField(required = True)
    billing_address_city = serializers.CharField(required = True)
    billing_address_phone = serializers.CharField(required = True)
    billing_address_name = serializers.CharField(required = True)
    billing_address_country = serializers.CharField(required = True)
    billing_address_zip_code = serializers.CharField(required = True)
    shipping_address_address_line_1 = serializers.CharField(required = True)
    shipping_address_address_line_2 = serializers.CharField(required = False)
    shipping_address_city = serializers.CharField(required = True)
    shipping_address_state = serializers.CharField(required = True)
    shipping_address_phone = serializers.CharField(required = True)
    shipping_address_name = serializers.CharField(required = True)
    shipping_address_country = serializers.CharField(required = True)
    shipping_address_zip_code = serializers.CharField(required = True)
    cupon_code = serializers.CharField(required = False)

    
class DeleteOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class GetOrderByIdOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class OrderStatusResponseSerializers(serializers.Serializer):
    is_paid = serializers.BooleanField()
    is_shipped = serializers.BooleanField()
    is_delivered = serializers.BooleanField()
    is_completed = serializers.BooleanField()

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'membership_name', 'membership_price', 'membership_description', 'membership_image', 'membership_lifetime']

    