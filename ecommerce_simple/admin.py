from django.contrib import admin
from .models import *


# Register your models here.


class ProductSimpleAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image', 'stock')
    search_fields = ('name', 'price', 'description', 'image', 'stock')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name', 'image')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_name', 'membership_price', 'membership_description', 'membership_lifetime', 'membership_is_available', 'is_abstract')
    search_fields = ('membership_name', 'membership_price', 'membership_description', 'membership_lifetime', 'membership_is_available', 'is_abstract')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product', 'quantity')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'address_line_1', 'address_line_2', 'city', 'state', 'country')
    search_fields = ('name', 'address_line_1', 'address_line_2', 'city', 'state', 'country')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'billing_address', 'shipping_address', 'ip', 'is_paid', 'is_shipped', 'is_delivered', 'is_completed', 'tracking_number')
    search_fields = ('user', 'billing_address', 'shipping_address', 'ip', 'is_paid', 'is_shipped', 'is_delivered', 'is_completed', 'tracking_number')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(ProductSimple, ProductSimpleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryItem, GalleryItemAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(ProductVariable)
admin.site.register(CartItem, CartItemsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Order, OrderAdmin)

