from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='gameduo API',
        default_version='v1',
        description='gameduo-project',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
<<<<<<< HEAD
    path('users', include('user.urls')),
=======
    path('admin/', admin.site.urls),
    path('', include('dj_rest_auth.urls')),
    # path('accounts/', include('dj_rest_auth.registration.urls')),
    # path('users', include('user.urls')),
>>>>>>> 38910fb (로그인 시리얼라이저 추가 (#4))
]

urlpatterns += [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(r'^swagger$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
