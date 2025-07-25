from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _      
from django.core.exceptions import ValidationError

# Create your models here.
class Gender(models.TextChoices):
    MALE = 'Male', _('Male')
    FEMALE = 'Female', _('Female')

class Roles(models.TextChoices):
    ADMIN = 'Admin', _('Admin')
    FARMER = 'Farmer', _('Farmer')
    EXPERT = 'Expert', _('Expert')


class Tipscategory(models.TextChoices):
    CROP = 'Crop', _('Crop')
    LIVESTOCK = 'Livestock', _('Livestock')
    EQUIPMENT = 'Equipment', _('Equipment')
    OTHER = 'Other', _('Other')

class Crop(models.TextChoices):
    CORN = 'Corn', _('Corn')
    SOYBEAN = 'Soybean', _('Soybean')
    MAIZE = 'Maize', _('Maize')
    COTTON = 'Cotton', _('Cotton')
    OTHER = 'Other', _('Other')

class Livestock(models.TextChoices):
    COW = 'Cow', _('Cow')
    PIG = 'Pig', _('Pig')
    SHEEP = 'Sheep', _('Sheep')
    OTHER = 'Other', _('Other')

class Equipment(models.TextChoices):
    HOE = 'Hoe', _('Hoe')
    DRILL = 'Drill', _('Drill')
    CATERPILLAR = 'Caterpillar', _('Caterpillar')
    OTHER = 'Other', _('Other')


# user table
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE)
    role = models.CharField(max_length=10, choices=Roles.choices)


    def __str__(self):
        return self.username
    

# tips table
class Tip(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    category = models.CharField(max_length=20, choices=Tipscategory.choices)
    crop = models.CharField(max_length=20, choices=Crop.choices, null=True, blank=True)
    livestock = models.CharField(max_length=20, choices=Livestock.choices, null=True, blank=True)
    equipment = models.CharField(max_length=20, choices=Equipment.choices, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()
        if self.category == 'Crop' and not self.crop:
            raise ValidationError({'crop': 'Crop must be set when category is Crop.'})
        if self.category == 'Livestock' and not self.livestock:
            raise ValidationError({'livestock': 'Livestock must be set when category is Livestock.'})
        if self.category == 'Equipment' and not self.equipment:
            raise ValidationError({'equipment': 'Equipment must be set when category is Equipment.'})

        # Ensure only one of the three fields is filled
        filled_fields = [bool(self.crop), bool(self.livestock), bool(self.equipment)]
        if sum(filled_fields) > 1:
            raise ValidationError("Only one of crop, livestock, or equipment should be filled based on the selected category.")



    def __str__(self):
        return self.title
    


# pests and diseases table
class PestDisease(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    category = models.CharField(max_length=20, choices=Tipscategory.choices)
    crop = models.CharField(max_length=20, choices=Crop.choices, null=True, blank=True)
    livestock = models.CharField(max_length=20, choices=Livestock.choices, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()
        if self.category == 'Crop' and not self.crop:
            raise ValidationError({'crop': 'Crop must be set when category is Crop.'})
        if self.category == 'Livestock' and not self.livestock:
            raise ValidationError({'livestock': 'Livestock must be set when category is Livestock.'})
        
        # Ensure only one of the two fields is filled
        filled_fields = [bool(self.crop), bool(self.livestock)]
        if sum(filled_fields) > 1:
            raise ValidationError("Only one of crop or livestock should be filled based on the selected category.")


    def __str__(self):
        return self.title