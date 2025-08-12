from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class TipListView(generics.ListAPIView):
    queryset = Tip.objects.all().order_by('-date')
    serializer_class = TipSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class TipDetailView(generics.RetrieveAPIView):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class PestsandDiseasesListView(generics.ListAPIView):
    queryset = PestsandDiseases.objects.all().order_by('-date')
    serializer_class = PestsandDiseasesSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class PestsandDiseasesDetailView(generics.RetrieveAPIView):
    queryset = PestsandDiseases.objects.all()
    serializer_class = PestsandDiseasesSerializer

    def get_serializer_context(self):
        return {'request': self.request}
