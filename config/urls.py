from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
# Swagger UI documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bunkie App API",
        default_version="v1",
        description="Bunkie API using Django rest framework",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="zuriteam@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # documentation urls
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),

    # browser login
    path("api-auth/", include("rest_framework.urls")),

    # api authentication and token generation
    path("user/", include("account.urls", namespace="accounts")),
]
