from cgi import FieldStorage
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from django.contrib.auth.models import User
from ecommerce_simple.models import *

@dataclass
class ProductSimpleCore:
    request : object = field(default_factory=object, init=True)
    model : object = field(default = ProductSimple, init=True)
    fields_product : Dict = field(default_factory=dict, init=False)
    fields_categories : Dict = field(default_factory=dict, init=False)
    fields_gallery : Dict = field(default_factory=dict, init=False)

    def __post_init__(self):
        self.fields_product = self.get_fields_product()
        self.fields_categories = self.get_fields_categories()
        self.fields_gallery = self.get_fields_gallery()


    def get_fields_product(self):
        if not self.request: raise Exception("No request object")
        try:
            fields = {
                "name" : self.request.POST.get("name"),
                "description" : self.request.POST.get("description"),
                "price" : self.request.POST.get("price"),
                "image" : self.request.FILES.get("image"),
                "sales_price" : self.request.POST.get("sales_price"),
                "is_featured" : self.request.POST.get("is_featured"),
                "is_on_sale" : self.request.POST.get("is_on_sale"),
                "is_new" : self.request.POST.get("is_new"),
                "is_published" : self.request.POST.get("is_published"),
                "product_id": self.request.POST.get("product_id"),
            }
        except:
            raise Exception("Error getting fields")
        return fields

    def get_fields_categories(self):
        if not self.request: raise Exception("No request object")
        fields = {}
        try:
            for category in self.request.POST.getlist("category"):
                categories = Category.objects.filter(name=category)
                if categories:
                    fields[category] = categories[0]

        except:
            raise Exception("Error getting categories fields")

        return fields

    def get_fields_gallery(self):
        if not self.request: raise Exception("No request object")
        fields = {}
        return fields

    def __str__(self):
        return "ProductSimpleCore"

    def create(self):
        field = ''
        return self.model.objects.create
        