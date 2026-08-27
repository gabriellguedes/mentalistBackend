from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, CustomTokenObtainPairView, RegisterView, me_view

router = DefaultRouter()
router.register(r'entities/User', UserViewSet, basename='user')

urlpatterns = [ 
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', me_view, name='user-me'),
    path('', include(router.urls)),
]