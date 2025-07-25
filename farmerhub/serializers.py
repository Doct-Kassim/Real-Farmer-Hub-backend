from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

# serializer specifically for login
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Validate username and password first
        data = super().validate(attrs)

        user = self.user

        # Optionally, add role to token response
        data['id'] = user.id
        data['username'] = user.username
        data['role'] = user.role
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        return data
    







#  userprofile serializer
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    new_password = serializers.CharField(write_only=True, required=False)
    verify_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'new_password', 'verify_password')

    def validate(self, data):
        new_password = data.get('new_password')
        verify_password = data.get('verify_password')

        # If either is provided, both must be present and match
        if new_password or verify_password:
            if not new_password:
                raise serializers.ValidationError({"new_password": "This field is required."})
            if not verify_password:
                raise serializers.ValidationError({"verify_password": "This field is required."})
            if new_password != verify_password:
                raise serializers.ValidationError({"verify_password": "Passwords do not match."})
            if len(new_password) < 4:
                raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long."})

        return data

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('verify_password', None)  # Remove it; only used for validation

        # Update fields like first_name, last_name, etc.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If new_password was provided, update password
        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance


# register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'address', 'gender', 'role', 'password', 'password2')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'phone': {'required': True},
            'address': {'required': True},
            'role': {'required': True},
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
            phone=validated_data['phone'],
            address=validated_data['address'],
            gender=validated_data['gender'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user
    

#  Tip serializer
from rest_framework import serializers
from .models import Tip

class TipSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Tip
        fields = [
            'id',
            'author',
            'category',
            'crop',
            'livestock',
            'equipment',
            'title',
            'description',
            'date',
            'updated_at'
        ]
        read_only_fields = ['date', 'updated_at']

    def validate(self, data):
        category = data.get('category')
        crop = data.get('crop')
        livestock = data.get('livestock')
        equipment = data.get('equipment')

        # Enforce one field only per category
        if category == 'Crop':
            if not crop:
                raise serializers.ValidationError({"crop": "This field is required when category is Crop."})
            if livestock or equipment:
                raise serializers.ValidationError("Only crop should be set when category is Crop.")
        elif category == 'Livestock':
            if not livestock:
                raise serializers.ValidationError({"livestock": "This field is required when category is Livestock."})
            if crop or equipment:
                raise serializers.ValidationError("Only livestock should be set when category is Livestock.")
        elif category == 'Equipment':
            if not equipment:
                raise serializers.ValidationError({"equipment": "This field is required when category is Equipment."})
            if crop or livestock:
                raise serializers.ValidationError("Only equipment should be set when category is Equipment.")
        else:
            raise serializers.ValidationError({"category": "Invalid category selected."})

        return data



class PestDiseaseSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = PestDisease
        fields = [
            'id',
            'author',
            'category',
            'crop',
            'livestock',
            'title',
            'description',
            'date',
            'updated_at'
        ]
        read_only_fields = ['date', 'updated_at']

    def validate(self, data):
        category = data.get('category')
        crop = data.get('crop')
        livestock = data.get('livestock')

        # Enforce one field only per category
        if category == 'Crop':
            if not crop:
                raise serializers.ValidationError({"crop": "This field is required when category is Crop."})
            if livestock:
                raise serializers.ValidationError("Only crop should be set when category is Crop.")
        elif category == 'Livestock':
            if not livestock:
                raise serializers.ValidationError({"livestock": "This field is required when category is Livestock."})
            if crop:
                raise serializers.ValidationError("Only livestock should be set when category is Livestock.")
        else:
            raise serializers.ValidationError({"category": "Invalid category selected."})

        return data
