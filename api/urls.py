from django.urls import path
from .views import (
    AccountListCreateView,
    AccountRetrieveUpdateDeleteView,
    EmailOTPSendView,
    EmailOTPLoginView
)

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('users/', AccountListCreateView.as_view(), name="create_and_get_users"),
    path('users/<str:id>/', AccountRetrieveUpdateDeleteView.as_view(), name="account_operations"),


    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='password_login'),
    path('auth/login/email/', EmailOTPSendView.as_view(), name="otp_login_send"),
    path('auth/login/verify/', EmailOTPLoginView.as_view({'post' : 'post'}), name="otp_login_verify"),


    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', jwt_views.TokenBlacklistView.as_view(), name='token_blacklist_and_delete'),
]


