"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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


from accounts.models import Accounts
from service.models import Service
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls", namespace="accounts")),
    path(
        "schema/",
        get_schema_view(
            title="Hostdog-API", description="API for Hostdog system", version="1.0.0"
        ),
        name="openapi-schema",
    ),
    path("", include_docs_urls(title="Hostdog-API")),
    path('api/service/', include('service.urls')),
]
