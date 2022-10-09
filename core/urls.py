"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from drf_yasg import openapi

api_info = openapi.Info(
    title="Horizon Ecommerce API",
    default_version='v1',
    description="API for the Ecommerce app",
    terms_of_service="https://horizon-development.com/terms/",
    contact=openapi.Contact(email="mateus@horizon-development.com", name="Mateus", url="https://horizon-development.com"),
    license=openapi.License(name="BSD License")
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(AllowAny,),
    url=settings.SITE_URL
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('api-auth/', include('accounts.urls', namespace='Accounts')),
    path('api-ecommerce/', include('ecommerce_simple.urls', namespace='Ecommerce')),
    path('docs/', TemplateView.as_view(
        template_name='dev/redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
    path('', TemplateView.as_view(
        template_name='dev/swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('openapi-schema/', schema_view.as_view(), name='openapi-schema'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
