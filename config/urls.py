"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from application.views import ReactAppView
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .settings import DEBUG
# Настройка схемы Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Business Programming",  
        default_version='v1',  # Версия API
        description="Cистема для упрощения образовательного процесса",  
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kalimullinbulat26@gmail.com"),
        license=openapi.License(name="@nollieundergrob"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("application.urls")),
    path("simple/", include("localpypi.urls")),
    path('tests/',include('testerapp.urls')),
    path('workflows/', include('labwork.urls')),
    re_path("^(?!admin/|users/|simple/|test/).*", ReactAppView.as_view(), name="home"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    swagger = [
         re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^doc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
    urlpatterns+=swagger