from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


class Profile(models.Model):
    EXPERIENCE_LEVELS = [
        ('fresher', 'Fresher'),
        ('junior', 'Junior (0-2 years)'),
        ('mid', 'Mid-level (2-5 years)'),
    ]
    
    CAREER_TRACKS = [
        ('web_dev', 'Web Development'),
        ('data_science', 'Data Science'),
        ('mobile_dev', 'Mobile Development'),
        ('ui_ux', 'UI/UX Design'),
        ('marketing', 'Digital Marketing'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # Profile Information
    education_level = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_LEVELS, 
        default='fresher'
    )
    career_track = models.CharField(
        max_length=50, 
        choices=CAREER_TRACKS, 
        blank=True
    )
    
    # Skills and Experience
    skills = models.JSONField(default=list, blank=True)
    experience_description = models.TextField(blank=True)
    cv_text = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
