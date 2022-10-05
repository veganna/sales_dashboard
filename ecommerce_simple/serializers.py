from inflection import tableize
from rest_framework import serializers
from .models import *
from accounts.models import User


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
        fields = ['image']

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

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'is_paid', 'total_items', 'is_shipped', 'is_delivered',  'is_completed', 'tracking_number', 'shipping_address', 'created_at', 'updated_at']

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
        return UserResponseSerializer(obj.user, many=False).data

    def get_items(self, obj):
        return CartItemSerializer(obj.items.all(), many=True).data


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'email', 'first_name', 'last_name', 'phone']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address', 'city', 'phone', 'name' ,'country', 'zip_code']

class OrderResponseSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserResponseSerializer(many=False)
    shipping_address = AddressSerializer(many=False)
    items = CartItemResponseSerializer(many=True)
    is_paid = serializers.BooleanField()
    is_shipped = serializers.BooleanField()
    is_delivered = serializers.BooleanField()
    is_completed = serializers.BooleanField()
    total_cost = serializers.IntegerField()
    total_items = serializers.IntegerField()

class CreateOrderSerializer(serializers.Serializer):
    country = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()
    address = serializers.CharField()
    zip_code = serializers.CharField()
    phone = serializers.CharField()

    
class DeleteOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class GetOrderByIdOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class OrderStatusResponseSerializers(serializers.Serializer):
    is_paid = serializers.BooleanField()
    is_shipped = serializers.BooleanField()
    is_delivered = serializers.BooleanField()
    is_completed = serializers.BooleanField()