from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'education_level', 'experience_level', 'career_track']
    search_fields = ['user__email', 'user__username']
    list_filter = ['experience_level', 'career_track']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
