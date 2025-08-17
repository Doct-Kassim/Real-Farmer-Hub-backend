from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

# -------------------------
# Existing User/Tip Models
# -------------------------

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

class CustomUserManager(UserManager):
    def create_user(self, username, email, password=None, phone=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Roles.ADMIN)
        extra_fields.setdefault("phone", None)
        extra_fields.setdefault("address", None)
        extra_fields.setdefault("gender", None)
        extra_fields.setdefault("first_name", None)
        extra_fields.setdefault("last_name", None)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password=password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.MALE, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.FARMER)
    first_name = models.CharField(max_length=150, blank=True, null=True)  
    last_name = models.CharField(max_length=150, blank=True, null=True)   

    objects = CustomUserManager()

    def __str__(self):
        return self.username  

# -------------------------
# Existing Tip & Photo Models
# -------------------------
class Tip(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    category = models.CharField(max_length=20, choices=Tipscategory.choices)
    crop = models.CharField(max_length=50, null=True, blank=True)
    livestock = models.CharField(max_length=50, null=True, blank=True)
    equipment = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video = models.FileField(upload_to='tip_videos/', null=True, blank=True)

    def clean(self):
        super().clean()
        if self.category == 'Crop' and not self.crop:
            raise ValidationError({'crop': 'Crop must be set when category is Crop.'})
        if self.category == 'Livestock' and not self.livestock:
            raise ValidationError({'livestock': 'Livestock must be set when category is Livestock.'})
        if self.category == 'Equipment' and not self.equipment:
            raise ValidationError({'equipment': 'Equipment must be set when category is Equipment.'})
        filled_fields = [bool(self.crop), bool(self.livestock), bool(self.equipment)]
        if sum(filled_fields) > 1:
            raise ValidationError("Only one of crop, livestock, or equipment should be filled based on the selected category.")
        if not self.pk:
            return
        has_photos = hasattr(self, 'photos') and self.photos.exists()
        if self.video and has_photos:
            raise ValidationError("You can upload either photo(s) or one video, not both.")
        if self.video:
            valid_extensions = ['.mp4', '.mov', '.avi']
            if not any(self.video.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError({'video': 'Unsupported video format. Use MP4, MOV, or AVI.'})
        if not self.video and not has_photos:
            raise ValidationError("You must upload either a video or at least one photo.") 

    def __str__(self):
        return self.title 

class TipPhoto(models.Model):
    tip = models.ForeignKey(Tip, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tip_photos/', null=True, blank=True)

    def __str__(self):
        return f"Photo for {self.tip.title}"

# -------------------------
# Existing Pests & Forum Models
# -------------------------
class PestsandDiseases(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    category = models.CharField(max_length=20, choices=Tipscategory.choices)
    crop = models.CharField(max_length=50, null=True, blank=True)
    livestock = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = RichTextUploadingField()
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video = models.FileField(upload_to='pestsanddiseases_videos/', null=True, blank=True)

    def clean(self):
        super().clean()
        if self.category == 'Crop' and not self.crop:
            raise ValidationError({'crop': 'Crop must be set when category is Crop.'})
        if self.category == 'Livestock' and not self.livestock:
            raise ValidationError({'livestock': 'Livestock must be set when category is Livestock.'})
        filled_fields = [bool(self.crop), bool(self.livestock)]
        if sum(filled_fields) > 1:
            raise ValidationError("Only one of crop, livestock should be filled based on the selected category.")
        if not self.pk:
            return
        has_photos = hasattr(self, 'photos') and self.photos.exists()
        if self.video and has_photos:
            raise ValidationError("You can upload either photo(s) or one video, not both.")
        if self.video:
            valid_extensions = ['.mp4', '.mov', '.avi']
            if not any(self.video.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError({'video': 'Unsupported video format. Use MP4, MOV, or AVI.'})

    def __str__(self):
        return self.title 

class PestsandDiseasesPhoto(models.Model):
    pestsanddiseases = models.ForeignKey(PestsandDiseases, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pestsanddiseases_photos/')

    def __str__(self):
        return f"Photo for {self.pestsanddiseases.title}"

class ForumRoom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(User, related_name='forum_rooms')
    
    def __str__(self):
        return self.name

class ForumMessage(models.Model):
    room = models.ForeignKey(ForumRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='forum/images/', blank=True, null=True)
    video = models.FileField(upload_to='forum/videos/', blank=True, null=True)
    file = models.FileField(upload_to='forum/files/', blank=True, null=True)
    voice_note = models.FileField(upload_to='forum/voice_notes/', blank=True, null=True)
    is_emoji = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Message by {self.sender.username} in {self.room.name}"
    
    def clean(self):
        if not any([self.content, self.image, self.video, self.file, self.voice_note]):
            raise ValidationError("Message must have content, image, video, file or voice note")

# -------------------------
# NEW Training & Tutorials Model
# -------------------------
class TrainingVideo(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_staff': True},  # Only staff/admin can be chosen as author
        related_name="training_videos"
    )
    title = models.CharField(max_length=200)
    description = RichTextUploadingField()
    video_file = models.FileField(upload_to='training_videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Training Video"
        verbose_name_plural = "Training Videos"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        if self.video_file:
            valid_extensions = ['.mp4', '.mov', '.avi']
            if not any(self.video_file.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError({'video_file': 'Unsupported video format. Use MP4, MOV, or AVI.'})
