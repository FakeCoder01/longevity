from django.urls import path
from .views import (
    AccountListCreateView,
    AccountRetrieveUpdateDeleteView,
    EmailOTPSendView,
    EmailOTPLoginView
)

from rest_framework_simplejwt import views as jwt_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
      title="Longevity API",
      default_version='v1'
    ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('users/', AccountListCreateView.as_view(), name="create_and_get_users"),
    path('users/<str:id>/', AccountRetrieveUpdateDeleteView.as_view(), name="account_operations"),


    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='password_login'),
    path('auth/login/email/', EmailOTPSendView.as_view(), name="otp_login_send"),
    path('auth/login/verify/', EmailOTPLoginView.as_view(), name="otp_login_verify"),


    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', jwt_views.TokenBlacklistView.as_view(), name='token_blacklist_and_delete'),
]


