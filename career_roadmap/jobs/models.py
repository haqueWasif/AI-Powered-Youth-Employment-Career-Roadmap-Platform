from django.db import models

class Job(models.Model):
    JOB_TYPES = [
        ('internship', 'Internship'),
        ('part_time', 'Part-time'),
        ('full_time', 'Full-time'),
        ('contract', 'Contract'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('fresher', 'Fresher'),
        ('junior', 'Junior (0-2 years)'),
        ('mid', 'Mid-level (2-5 years)'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    is_remote = models.BooleanField(default=False)
    
    # Job Details
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVELS,
        default='fresher'
    )
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES,
        default='full_time'
    )
    
    # Additional Info
    salary_range = models.CharField(max_length=100, blank=True)
    application_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
