from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    UpdateProfileView,
    TipListView,
    TipDetailView,
    PestsandDiseasesListView,
    PestsandDiseasesDetailView,
    UserProfileView,
    # Forum views
    ForumRoomViewSet,
    ForumMessageListView,
    ForumMessageDetailView,
    # TrainingVideo views
    TrainingVideoListView,
    TrainingVideoDetailView,
    
)

router = DefaultRouter()
router.register(r'forum/rooms', ForumRoomViewSet, basename='forumroom')


urlpatterns = [
    # Authentication URLs
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register-user/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile URLs
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),

    # Tips URLs
    path('tips/', TipListView.as_view(), name='tip-list'),
    path('tips/<int:pk>/', TipDetailView.as_view(), name='tip-detail'),

    # Pests and Diseases URLs
    path('pests-and-diseases/', PestsandDiseasesListView.as_view(), name='pestsanddiseases-list'),
    path('pests-and-diseases/<int:pk>/', PestsandDiseasesDetailView.as_view(), name='pestsanddiseases-detail'),

    # CKEditor URL
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # Forum URLs
    path('forum/rooms/<int:room_id>/messages/', ForumMessageListView.as_view(), name='room-messages'),
    path('forum/messages/<int:pk>/', ForumMessageDetailView.as_view(), name='message-detail'),

    # Training Video URLs
    path('training-videos/', TrainingVideoListView.as_view(), name='trainingvideo-list'),
    path('training-videos/<int:pk>/', TrainingVideoDetailView.as_view(), name='trainingvideo-detail'),

   
    path('', include(router.urls)),
]
