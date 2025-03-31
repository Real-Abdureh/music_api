from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Paylite API",
      default_version='v1',
      description="paylite backend api",
      terms_of_service="https://www.paylite.com/policies/terms/",
      contact=openapi.Contact(email="contact@paylite.local"),
      license=openapi.License(name="Orellions License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)






from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),  # Include authentication routes
    path('api/artists/', include('artists.urls')), # Include artist routes
    path('api/events/', include('events.urls')), # Include events routes
    path('api/bookings/', include('bookings.urls')), # Include bookings routes

]
