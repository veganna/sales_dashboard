from django.db import models

# Create your models here.

class BaseProducts(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="gallery/independent", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="gallery/independent", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.name

class Gallery(models.Model):
    name = models.CharField(max_length=255)
    items = models.ManyToManyField(GalleryItem)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductSimple(BaseProducts):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, blank=True, null=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    is_variable = models.BooleanField(default=False)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    category = models.ManyToManyField('Category')

    class Meta:
        verbose_name_plural = "Products"

class ProductVariable(models.Model):
    _product_variants = models.ManyToManyField(ProductSimple, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank = True, null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to="gallery/independent", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock = models.IntegerField(default=0)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    category = models.ManyToManyField('Category')

    def get_total_stock(self):
        total_stock = 0
        for variant in range(len(self._product_variants.all())):
            if self._product_variants[variant].is_variable:
                total_stock += self._product_variants[variant].stock
        return total_stock

    def get_main_product(self):
        return self._product_variants.objects.all()[0]

    def save(self, *args, **kwargs):
        try:
            variations = self._product_variants.all()
            self.name = variations[0].name
            self.description = variations[0].description
            self.price = variations[0].price
            self.image = variations[0].image
            self.sales_price = variations[0].sales_price
            self.is_featured = variations[0].is_featured
            self.is_on_sale = variations[0].is_on_sale
            self.is_new = variations[0].is_new
            self.is_best_seller = variations[0].is_best_seller
            self.is_available = variations[0].is_available
            self.is_published = variations[0].is_published
            self.tax = variations[0].tax
            self.category = variations[0].category
            self.stock = self.get_total_stock()
            super(ProductVariable, self).save(*args, **kwargs)
        except:
            super(ProductVariable, self).save(*args, **kwargs)
        

class Service(BaseProducts):
    pass

class CartItem(models.Model):
    product = models.ForeignKey(ProductSimple, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

class Cart(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, null=True)
    items = models.ManyToManyField(CartItem, blank=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.price
        return total

    def get_total_items(self):
        total = 0
        for item in self.items.all():
            total += 1
        return total

    def __str__(self):
        return self.user.email

class Address(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
    items = models.ManyToManyField(CartItem, blank=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.price
        return total

    def get_total_items(self):
        total = 0
        for item in self.items.all():
            total += 1
        return total

    def __str__(self):
        return self.user.email

