"""social_network URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from accounts import views as acc_view
from posts import views as posts_view

acc_router = DefaultRouter()
acc_router.register('register', acc_view.ProfileRegisterAPIView)

posts_router = DefaultRouter()
posts_router.register('tweet', posts_view.TweetViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Twitter Clone API",
      default_version='v-0.01-alpha',
      description="This API for working Twitter API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="sultanu@inbox.ru"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
   # path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/auth/token', obtain_auth_token),
    path('api/auth/', include('rest_framework.urls')),

    path('api/accounts/', include(acc_router.urls)),
    path('api/posts/', include(posts_router.urls)),
    path('api/posts/statustype/', posts_view.StatusTypeCreateListView.as_view()),
    path('api/posts/tweet/<int:tweet_id>/comment/', posts_view.CommentListCreateAPIView.as_view()),

    #documentation

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),

]

# urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#    ...
# ]