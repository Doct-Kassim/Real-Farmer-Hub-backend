from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import (
    User, Tip, TipPhoto, 
    PestsandDiseases, PestsandDiseasesPhoto, 
    ForumRoom, ForumMessage, TrainingVideo
)

# ------------------------
# Custom User Forms
# ------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'phone', 'address', 
            'gender', 'role', 'first_name', 'last_name'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'phone', 'address', 'gender', 
            'role', 'first_name', 'last_name', 
            'is_active', 'is_staff', 'is_superuser'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('password')
        if raw_password and not raw_password.startswith('pbkdf2_sha256$'):
            user.set_password(raw_password)
        if commit:
            user.save()
        return user


# ------------------------
# Custom User Admin
# ------------------------
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'address', 'gender', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 
                'phone', 'address', 'gender', 'role', 
                'first_name', 'last_name', 'is_staff', 'is_superuser'
            ),
        }),
    )

admin.site.register(User, CustomUserAdmin)


# ------------------------
# Tip Admin
# ------------------------
class TipPhotoInline(admin.TabularInline):
    model = TipPhoto
    extra = 1

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    inlines = [TipPhotoInline]
    list_display = ['title', 'author', 'category', 'date', 'updated_at']
    search_fields = ['title', 'author__username', 'category']
    ordering = ['-date']


# ------------------------
# Pests and Diseases Admin
# ------------------------
class PestsandDiseasesPhotoInline(admin.TabularInline):
    model = PestsandDiseasesPhoto
    extra = 1

@admin.register(PestsandDiseases)
class PestsandDiseasesAdmin(admin.ModelAdmin):
    inlines = [PestsandDiseasesPhotoInline]
    list_display = ['title', 'author', 'category', 'date', 'updated_at']
    search_fields = ['title', 'author__username', 'category']
    ordering = ['-date']


# ------------------------
# Forum Admin
# ------------------------
admin.site.register(ForumRoom)
admin.site.register(ForumMessage)


# ------------------------
# TrainingVideo Admin
# ------------------------
@admin.register(TrainingVideo)
class TrainingVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']   # display title na created_at
    search_fields = ['title']
    ordering = ['-created_at']               # change from -uploaded_at to -created_at
    list_filter = ['created_at']             # change from uploaded_at to created_at
