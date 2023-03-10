"""youtubeClone URL Configuration

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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter

from core import views
from action import views as action_views

from rest_framework import permissions

from rest_framework_nested import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls")),
]


urlpatterns += [
    path("list-channels", views.ChannelListApiView.as_view(), name='list-channels')
]

router = DefaultRouter()

router.register('categorys', views.CategoryApiModelViewSet, basename='categorys')
router.register('channels', views.ChannelApiModelViewSet, basename='channels')
router.register('subscriptions', action_views.SubscriptionCreateEdtModelViewSet, basename='subscriptions')
router.register("likes", action_views.LikeCreateEdtModelViewSet, basename="likes")
router.register("dislikes", action_views.DislikeCreateEdtModelViewSet, basename="dislikes")


channel_router = routers.NestedDefaultRouter(router, 'channels',lookup='channel')
channel_router.register("contents", views.ContentApiModelViewSet, basename='channel-contents')
channel_router.register("subscribers", action_views.SubscriptionModelViewSet, basename="subscribers")


content_router = routers.NestedDefaultRouter(channel_router, 'contents', lookup='content')
content_router.register("comments", views.CommentApiModelViewSet, basename='content-comments')
content_router.register("likes", action_views.LikeModelViewSet, basename='content-likes')
content_router.register("dislikes", action_views.DislikeModelViewSet, basename='content-dislikes')
content_router.register("views", action_views.ViewModelViewSet, basename='content-views')

urlpatterns += router.urls + channel_router.urls + content_router.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

schema_view = get_schema_view(
   openapi.Info(
      title="Income Tracker API",
      default_version='v1',
      description="Endpoints for Income and Expences Tracker Api",
      terms_of_service="https://www.myapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@income.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^swagger/apiJson$', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]