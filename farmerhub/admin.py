from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, Tip, TipPhoto, PestsandDiseases, PestsandDiseasesPhoto

# Custom forms for User creation and editing
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone', 'address', 'gender', 'role', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Always hash password properly
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'address', 'gender', 'role', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Only hash password if changed and not already hashed
        raw_password = self.cleaned_data.get('password')
        if raw_password and not raw_password.startswith('pbkdf2_sha256$'):
            user.set_password(raw_password)
        if commit:
            user.save()
        return user

# Custom User Admin class
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'address', 'gender', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone', 'address', 'gender', 'role', 'first_name', 'last_name', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(User, CustomUserAdmin)


# Inline for TipPhoto, so admin can add multiple photos directly in Tip form
class TipPhotoInline(admin.TabularInline):
    model = TipPhoto
    extra = 1  # Show one extra empty field by default

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    inlines = [TipPhotoInline]
    list_display = ['title', 'author', 'category', 'date', 'updated_at']
    search_fields = ['title', 'author__username', 'category']
    ordering = ['-date']

    def save_model(self, request, obj, form, change):
        # Save the Tip instance
        super().save_model(request, obj, form, change)
        # Additional processing for videos or other fields can be added here if needed


# Inline for PestsandDiseasesPhoto for the same reason
class PestsandDiseasesPhotoInline(admin.TabularInline):
    model = PestsandDiseasesPhoto
    extra = 1

@admin.register(PestsandDiseases)
class PestsandDiseasesAdmin(admin.ModelAdmin):
    inlines = [PestsandDiseasesPhotoInline]
    list_display = ['title', 'author', 'category', 'date', 'updated_at']
    search_fields = ['title', 'author__username', 'category']
    ordering = ['-date']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Add any extra processing for video here if needed
