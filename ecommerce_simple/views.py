from drf_yasg import openapi as OA
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .cart import CartCore
from .order import OrderCore
# Create your views here.

class GetAllProductsView(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    product_simple_sample = ProductSimpleSerializer(many=True)
    product_variable_sample = ProductVariableSerializer(many=False)

    @swagger_auto_schema(
        operation_description="Get all products (Auth not required)",
        operation_id="Get all products",
        operation_summary="Get all products (Auth not required)",
        tags=['Products'],
        responses = {
            200: GetAllProductsSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        products_simple = ProductSimple.objects.filter(is_variable=False)
        serializer_simple = ProductSimpleSerializer(products_simple, many=True)
        products_variable = ProductVariableSerializer(ProductVariable.objects.filter(is_available = True), many=True)

        return Response(
            {
                'products_simple': serializer_simple.data,
                'products_variable': products_variable.data
            }, 
            status=status.HTTP_200_OK
        )

class GetProductView(generics.GenericAPIView):
    permission_classes = [AllowAny,]

    @swagger_auto_schema(
        operation_description="Get product by id (Auth Not Required)",
        operation_id="Get product by id ",
        operation_summary="Get product by id (Auth Not Required)",
        tags=['Products'],
        manual_parameters=[
            OA.Parameter(
                name="id",
                in_=OA.IN_PATH,
                description="Product id",
                required=True,
                type=OA.TYPE_INTEGER
            )
        ],
        responses = {
            200: ProductSimpleSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request, id):
        try:
            product_simple = ProductSimple.objects.get(id=id)
            serializer_simple = ProductSimpleSerializer(product_simple, many=False)

            return Response(
                serializer_simple.data,
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {
                    'message': 'Product not found'
                }, 
                status=status.HTTP_404_NOT_FOUND
            )

class FilterProductsView(generics.GenericAPIView):
    permission_classes = [AllowAny,]

    @swagger_auto_schema(
        operation_description="Filter products (Auth Not Required)",
        operation_id="Filter products",
        operation_summary="Filter products (Auth Not Required)",
        tags=['Products'],
        manual_parameters=[
            OA.Parameter(
                name="categories",
                in_=OA.IN_QUERY,
                description="Categories name",
                required=False,
                type=OA.TYPE_ARRAY,
                items=OA.Items(type=OA.TYPE_STRING)
            ),
            OA.Parameter(
                name="price_min",
                in_=OA.IN_QUERY,
                description="Minimum price",
                required=False,
                type=OA.TYPE_INTEGER,
            ),
            OA.Parameter(
                name="price_max",
                in_=OA.IN_QUERY,
                description="Maximum price",
                required=False,
                type=OA.TYPE_INTEGER,
            ),
            OA.Parameter(
                name="search",
                in_=OA.IN_QUERY,
                description="Search",
                required=False,
                type=OA.TYPE_STRING,
            )
        ],
        responses = {
            200: GetAllProductsSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        category = request.GET.get('category')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        search = request.GET.get('search')
        category = category.split(',') if category else None

        if category:
            products_simple = ProductSimple.objects.filter(category__name__in=category, is_variable=False, is_available=True)
            products_variable = ProductVariable.objects.filter(category__name__in=category, is_available=True)
        else:
            products_simple = ProductSimple.objects.filter(is_variable=False, is_available=True)
            products_variable = ProductVariable.objects.filter(is_available=True)

        if price_min:
            products_simple = products_simple.filter(price__gte=price_min)
            products_variable = products_variable.filter(price__gte=price_min)

        if price_max:
            products_simple = products_simple.filter(price__lte=price_max)
            products_variable = products_variable.filter(price__lte=price_max)

        if search:
            products_simple = products_simple.filter(name__icontains=search)
            products_variable = products_variable.filter(name__icontains=search)

        serializer_simple = ProductSimpleSerializer(products_simple, many=True)
        products_variable = ProductVariableSerializer(products_variable, many=True)

        return Response(
            {
                'products_simple': serializer_simple.data,
                'products_variable': products_variable.data
            }, 
            status=status.HTTP_200_OK
        )
        

        
        
class GetAllCategoriesView(generics.GenericAPIView):
    permission_classes = [AllowAny,]

    @swagger_auto_schema(
        operation_description="Get all categories (Auth Not Required)",
        operation_id="Get all categories",
        operation_summary="Get all categories (Auth Not Required)",
        tags=['Products Utils'],
        responses = {
            200: CategorySerializer(many=True),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class GetCart(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartSerializer

    @swagger_auto_schema(
        operation_description="Get user cart items (Authenticated)",
        operation_id="Get user cart items (Authenticated)",
        operation_summary="Get cart items (Auth required)",
        tags=['Cart'],
        manual_parameters=[
            OA.Parameter(
                name="IP",
                in_=OA.IN_QUERY,
                description="User IP",
                required=False,
                type=OA.TYPE_STRING
            )
        ],
        responses = {
            200: CartResponseSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        user = request.user
        cart = CartCore(user).get_cart()
        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )

class AddToCart(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartSerializer

    @swagger_auto_schema(
        operation_description="Add product to cart (Authenticated)",
        operation_id="Add product to cart (Authenticated)",
        operation_summary="Add product to cart (Auth required)",
        tags=['Cart'],
        request_body=AddToCartSerializer,
        responses = {
            200: CartResponseSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def post(self, request):
        user = request.user
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data.get('product_id')
        quantity = serializer.validated_data.get('quantity')
        cart = CartCore(user).add_to_cart(product_id, quantity)
        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )

class RemoveFromCart(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartSerializer

    @swagger_auto_schema(
        operation_description="Remove product from cart (Authenticated)",
        operation_id="Remove product from cart (Authenticated)",
        operation_summary="Remove product from cart (Auth required)",
        tags=['Cart'],
        request_body=AddToCartSerializer,
        responses = {
            200: CartResponseSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def put(self, request):
        user = request.user
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data.get('product_id')
        quantity = serializer.validated_data.get('quantity')
        cart = CartCore(user).remove_from_cart(product_id, quantity)
        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )
    
class DeleteCart(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartSerializer

    @swagger_auto_schema(
        operation_description="Delete user cart (Authenticated)",
        operation_id="Delete user cart (Authenticated)",
        operation_summary="Delete user cart (Auth required)",
        tags=['Cart'],
        responses = {
            200: "Cart Deleted",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def delete(self, request):
        user = request.user
        CartCore(user).delete_cart()
        return Response(
            {"message": "Cart Deleted"},
            status=status.HTTP_200_OK
        )

class CreateOrder(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="Create order (Auth required)",
        operation_id="Create order (Authenticated)",
        operation_summary="Create order (Auth required)",
        tags=['Order'],
        request_body=CreateOrderSerializer(many=False),
        responses = {
            200: OrderResponseSerializers(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def post(self, request):
        user = request.user
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        country = serializer.validated_data.get('country')
        city = serializer.validated_data.get('city')
        address = serializer.validated_data.get('address')
        state = serializer.validated_data.get('state')
        zip_code = serializer.validated_data.get('zip_code')
        name = request.user.first_name+" "+request.user.last_name
        phome = request.user.phone if request.user.phone else "0000000000"
        order = OrderCore(user).create_order(
            name=name,
            phone=phome,
            country=country,
            city=city,
            address=address,
            state=state,
            zip_code=zip_code
        )
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK
        )

class GetOrder(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="Get user orders (Auth required)",
        operation_id="Get user orders (Authenticated)",
        operation_summary="Get user orders (Auth required)",
        tags=['Order'],
        responses = {
            200: OrderResponseSerializers(many=True),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        user = request.user
        orders = OrderCore(user).get_orders()
        return Response(
            OrderSerializer(orders, many=True).data,
            status=status.HTTP_200_OK
        )

class GetOrderById(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="Get user order by id (Auth required)",
        operation_id="Get user order by id (Authenticated)",
        operation_summary="Get user order by id (Auth required)",
        tags=['Order'],
        responses = {
            200: OrderResponseSerializers(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request, order_id):
        user = request.user
        order = OrderCore(user).get_order(order_id)
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK
        )

class DeleteOrder(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        operation_description="Delete user order by id (Auth required)",
        operation_id="Delete user order by id (Authenticated)",
        operation_summary="Delete user order by id (Auth required)",
        tags=['Order'],
        manual_parameters=[
            OA.Parameter(
                name='order_id',
                in_=OA.IN_PATH,
                description='Order Id',
                type=OA.TYPE_INTEGER
            )
        ],
        responses = {
            200: "Order Deleted",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def delete(self, request, order_id):
        user = request.user
        OrderCore(user).delete_order(order_id)
        return Response(
            {"message": "Order Deleted"},
            status=status.HTTP_200_OK
        )



            

        