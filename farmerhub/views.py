from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import (
    ForumRoom, ForumMessage, Tip, PestsandDiseases, TrainingVideo
)
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    RegisterSerializer,
    TipSerializer,
    PestsandDiseasesSerializer,
    ForumRoomSerializer,
    ForumMessageSerializer,
    TrainingVideoSerializer
)

User = get_user_model()

# ------------------------
# Auth / User Views
# ------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return the logged-in user
        return User.objects.filter(id=self.request.user.id)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# ------------------------
# Tip / Pests Views
# ------------------------
class TipListView(generics.ListAPIView):
    queryset = Tip.objects.all().order_by('-date')
    serializer_class = TipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}


class TipDetailView(generics.RetrieveAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}


class PestsandDiseasesListView(generics.ListAPIView):
    queryset = PestsandDiseases.objects.all().order_by('-date')
    serializer_class = PestsandDiseasesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}


class PestsandDiseasesDetailView(generics.RetrieveAPIView):
    queryset = PestsandDiseases.objects.all()
    serializer_class = PestsandDiseasesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}


# ------------------------
# Forum Views
# ------------------------
class ForumRoomViewSet(viewsets.ModelViewSet):
    queryset = ForumRoom.objects.all()
    serializer_class = ForumRoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        room = serializer.save()
        room.participants.add(self.request.user)


class ForumMessageListView(generics.ListCreateAPIView):
    serializer_class = ForumMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return ForumMessage.objects.filter(room_id=room_id).order_by('timestamp')

    def perform_create(self, serializer):
        room_id = self.kwargs['room_id']
        room = ForumRoom.objects.get(id=room_id)
        serializer.save(sender=self.request.user, room=room)


class ForumMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ForumMessage.objects.all()
    serializer_class = ForumMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only edit/delete their own messages
        return ForumMessage.objects.filter(sender=self.request.user)


# ------------------------
# TrainingVideo Views
# ------------------------
class TrainingVideoListView(generics.ListCreateAPIView):
    queryset = TrainingVideo.objects.all().order_by('-created_at')
    serializer_class = TrainingVideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        # Only admin can upload videos
        if self.request.user.role != 'Admin':
            raise PermissionError("Only admin can upload training videos.")
        # Automatically assign author
        serializer.save(author=self.request.user)


class TrainingVideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TrainingVideo.objects.all()
    serializer_class = TrainingVideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
        if self.request.user.role != 'Admin':
            raise PermissionError("Only admin can update training videos.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.role != 'Admin':
            raise PermissionError("Only admin can delete training videos.")
        instance.delete()







