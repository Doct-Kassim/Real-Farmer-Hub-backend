from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Tip, TipPhoto, PestsandDiseases, PestsandDiseasesPhoto

User = get_user_model()

# --- Login Serializer with extra user info in token ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'gender': user.gender,
            'email': user.email,
            'phone': user.phone,
        })
        return data

# --- User Serializer for profile view/update ---
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    new_password = serializers.CharField(write_only=True, required=False)
    verify_password = serializers.CharField(write_only=True, required=False)

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'phone',
            'gender', 'email', 'role', 'new_password', 'verify_password'
        )

    def validate(self, data):
        new_password = data.get('new_password')
        verify_password = data.get('verify_password')

        if new_password or verify_password:
            if not new_password:
                raise serializers.ValidationError({"new_password": "This field is required."})
            if not verify_password:
                raise serializers.ValidationError({"verify_password": "This field is required."})
            if new_password != verify_password:
                raise serializers.ValidationError({"verify_password": "Passwords do not match."})
            if len(new_password) < 8:
                raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long."})

        return data

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('verify_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance

# --- Registration Serializer ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'address', 'gender', 'role', 'password', 'password2'
        )
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'address': {'required': True},
            'role': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            gender=validated_data['gender'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user

# --- TipPhoto Serializer (media URLs) ---
class TipPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TipPhoto
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

# --- Tip Serializer including media (photos/videos) ---
class TipSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    date_posted = serializers.DateTimeField(source='date', format="%Y-%m-%d %H:%M")
    last_updated = serializers.DateTimeField(source='updated_at', format="%Y-%m-%d %H:%M")

    class Meta:
        model = Tip
        fields = [
            'id', 'title', 'description', 'category',
            'crop', 'livestock', 'equipment',
            'author_name', 'media', 'date_posted', 'last_updated'
        ]

    def get_author_name(self, obj):
        full_name = f"{obj.author.first_name or ''} {obj.author.last_name or ''}".strip()
        return full_name if full_name else obj.author.username

    def get_media(self, obj):
        request = self.context.get('request')
        if not obj.pk:
            return None  # Avoid errors on unsaved instances

        if obj.video:
            return {
                'type': 'video',
                'url': request.build_absolute_uri(obj.video.url)
            }
        photos = obj.photos.all() if hasattr(obj, 'photos') else []
        if photos:
            return {
                'type': 'photos',
                'urls': [request.build_absolute_uri(photo.image.url) for photo in photos]
            }
        return None

# --- PestsandDiseasesPhoto Serializer ---
class PestsandDiseasesPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PestsandDiseasesPhoto
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

# --- PestsandDiseases Serializer including media ---
class PestsandDiseasesSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    date_posted = serializers.DateTimeField(source='date', format="%Y-%m-%d %H:%M")
    last_updated = serializers.DateTimeField(source='updated_at', format="%Y-%m-%d %H:%M")

    class Meta:
        model = PestsandDiseases
        fields = [
            'id', 'title', 'description', 'category',
            'crop', 'livestock',
            'author_name', 'media', 'date_posted', 'last_updated'
        ]

    def get_author_name(self, obj):
        full_name = f"{obj.author.first_name or ''} {obj.author.last_name or ''}".strip()
        return full_name if full_name else obj.author.username

    def get_media(self, obj):
        request = self.context.get('request')
        if not obj.pk:
            return None

        if obj.video:
            return {
                'type': 'video',
                'url': request.build_absolute_uri(obj.video.url)
            }
        photos = obj.photos.all() if hasattr(obj, 'photos') else []
        if photos:
            return {
                'type': 'photos',
                'urls': [request.build_absolute_uri(photo.image.url) for photo in photos]
            }
        return None
