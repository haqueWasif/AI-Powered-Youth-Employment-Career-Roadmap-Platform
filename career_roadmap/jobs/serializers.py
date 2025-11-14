from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    matched_skills = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'company',
            'location',
            'is_remote',
            'description',
            'required_skills',
            'experience_level',
            'job_type',
            'salary_range',
            'application_url',
            'created_at',
            'matched_skills'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_matched_skills(self, obj):
        """Calculate matched skills if user is authenticated"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                user_skills = set(request.user.profile.skills)
                job_skills = set(obj.required_skills)
                matched = list(user_skills.intersection(job_skills))
                return matched
            except:
                return []
        return []


class JobListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list view"""
    
    class Meta:
        model = Job
        fields = [
            'id',
            'title',
            'company',
            'location',
            'is_remote',
            'required_skills',
            'experience_level',
            'job_type',
            'salary_range'
        ]
