from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
# router.register(r'profile', UserProfileView, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    
    # login url
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # register url
    path('register-user/', RegisterView.as_view(), name='register'),
    
    # refresh token url
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # update profile url
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),

    # tips urls
    path('tips/', TipListView.as_view(), name='tip-list'),
    path('tips/<int:pk>/', TipDetailView.as_view(), name='tip-detail'),

    # pests and diseases urls
    path('pests-and-diseases/', PestsandDiseasesListView.as_view(), name='pestsanddiseases-list'),
    path('pests-and-diseases/<int:pk>/', PestsandDiseasesDetailView.as_view(), name='pestsanddiseases-detail'),

    # CKEditor uploader urls - hii ni muhimu kwa CKEditor file uploads
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
