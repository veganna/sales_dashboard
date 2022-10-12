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
from .member import MemberCore
from accounts.serializers import UserSerializer

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

class GetFecturedProductsView(generics.GenericAPIView):
    permission_classes = [AllowAny,]

    @swagger_auto_schema(
        operation_description="Get featured products (Auth Not Required)",
        operation_id="Get featured products",
        operation_summary="Get featured products (Auth Not Required)",
        tags=['Products Utils'],
        responses = {
            200: ProductSimpleSerializer(many=True),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        products_simple = ProductSimple.objects.filter(is_variable=False, is_featured=True)
        serializer_simple = ProductSimpleSerializer(products_simple, many=True)
        products_variable = ProductVariableSerializer(ProductVariable.objects.filter(is_available = True, is_featured=True), many=True)

        return Response(
            {
                'products_simple': serializer_simple.data,
                'products_variable': products_variable.data
            }, 
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
        order = OrderCore(user).create_order(serializer.validated_data)
            
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

class GetMembers(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Get members (Auth not required)",
        operation_id="Get members (Auth not required)",
        operation_summary="Get members (Auth not required)",
        tags=['Members'],
        responses = {
            200: UserSerializer(many=True),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        user = request.user
        member_core = MemberCore(user)

        members = member_core.get_members()
        if members:
            return Response(
                UserSerializer(members, many=True).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "No members found"},
            status=status.HTTP_200_OK
        )
class GetMemberById(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Get member by id (Auth required)",
        operation_id="Get member by id (Authenticated)",
        operation_summary="Get member by id (Auth required)",
        tags=['Members'],
        responses = {
            200: UserSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request, user_id):
        user = request.user
        member_core = MemberCore(user)
        if not member_core.is_member():
            return Response(
                {"message": "You are not a member"},
                status=status.HTTP_200_OK
            )

        member = member_core.get_member(user_id)
        if member:
            return Response(
                UserSerializer(member).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "No member found"},
            status=status.HTTP_200_OK
        )

class GetUserMembership(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = MembershipSerializer

    @swagger_auto_schema(
        operation_description="Get user membership (Auth required)",
        operation_id="Get user membership (Authenticated)",
        operation_summary="Get user membership (Auth required)",
        tags=['Members'],
        responses = {
            200: MembershipSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        user = request.user
        member_core = MemberCore(user)
        if not member_core.is_member():
            return Response(
                {"message": "You are not a member"},
                status=status.HTTP_200_OK
            )

        membership = member_core.get_membership()
        if membership:
            return Response(
                MembershipSerializer(membership).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "No membership found"},
            status=status.HTTP_200_OK
        )
    
class GetMemberPlans(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = MembershipSerializer

    @swagger_auto_schema(
        operation_description="Get member plans (Auth not required)",
        operation_id="Get member plans (Auth not required)",
        operation_summary="Get member plans (Auth not required)",
        tags=['Members Utils'],
        responses = {
            200: MembershipSerializer(many=True),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        plans = Membership.objects.filter(is_abstract = True)
        if plans:
            return Response(
                MembershipSerializer(plans, many=True).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "No plans found"},
            status=status.HTTP_200_OK
        )
class GetPlanById(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = MembershipSerializer

    @swagger_auto_schema(
        operation_description="Get plan by id (Auth not required)",
        operation_id="Get plan by id (Auth not required)",
        operation_summary="Get plan by id (Auth not required)",
        tags=['Members Utils'],
        responses={
            200: MembershipSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request, plan_id):
        plan = Membership.objects.filter(is_abstract = True, id = plan_id).first()
        if plan:
            return Response(
                MembershipSerializer(plan).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "No plan found"},
            status=status.HTTP_200_OK
        )

class GetTax(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = TaxSerializer

    @swagger_auto_schema(
        operation_description="Get tax (Auth not required)",
        operation_id="Get tax (Auth not required)",
        operation_summary="Get tax (Auth not required)",
        tags=['Order Utils'],
        manual_parameters = [
            OA.Parameter(
                'state',
                OA.IN_QUERY,
                description="State",
                type=OA.TYPE_STRING,
                required=False
            ),
            OA.Parameter(
                'zip_code',
                OA.IN_QUERY,
                description="Zip Code",
                type=OA.TYPE_STRING,
                required=False
            )
        ],
        responses = {
            200: TaxSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        if not request.GET.get('state') and not request.GET.get('zip_code'): 
            return Response(
                {"message": "State or zip code required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        tax = None
        if request.GET.get('zip_code'):
            tax = Tax.objects.filter(state = request.GET.get('zip_code')).first()
        elif request.GET.get('state'):
            tax = Tax.objects.filter(zip_code = request.GET.get('state')).first()
        if tax:
            return Response(
                TaxSerializer(tax).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "No tax found"},
            status=status.HTTP_404_NOT_FOUND
        )

class ValidateCoupon(generics.GenericAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CouponSerializer

    @swagger_auto_schema(
        operation_description="Validate coupon (Auth not required)",
        operation_id="Validate coupon (Auth not required)",
        operation_summary="Validate coupon (Auth not required)",
        tags=['Order Utils'],
        manual_parameters = [
            OA.Parameter(
                'code',
                OA.IN_QUERY,
                description="Coupon code",
                type=OA.TYPE_STRING,
                required=True
            )
        ],
        responses = {
            200: CouponSerializer(many=False),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }
    )
    def get(self, request):
        if not request.GET.get('code'): 
            return Response(
                {"message": "Coupon code required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        coupon = Coupon.objects.filter(code = request.GET.get('code')).first()
        if coupon:
            if coupon.is_expired():
                return Response(
                    {"message": "Coupon expired"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if coupon.is_used():
                return Response(
                    {"message": "Coupon used"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                CouponSerializer(coupon).data,
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "No coupon found"},
            status=status.HTTP_404_NOT_FOUND
        )