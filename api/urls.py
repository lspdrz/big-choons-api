from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tracks', views.TrackViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/obtain/',
         views.TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/token/refresh/',
         views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/google/', views.GoogleAuthView.as_view(), name='google'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
]
