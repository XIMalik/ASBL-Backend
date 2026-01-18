from rest_framework import serializers
from .models import Profile, Program, Person, ProgramPerson, News


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name', 'description', 'duration', 'level', 'category', 
                 'students', 'key_topics', 'additional_details', 'certificate_available',
                 'certificate_description', 'total_reviews', 'instructor_name', 'instructor_bio',
                 'instructor_image_url', 'thumbnail_url', 'video_intro_url', 'tagline',
                 'is_featured', 'start_date', 'end_date', 'schedule', 'price',
                 'image_urls', 'learning_outcomes', 'learning_approach',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'position', 'bio', 'email', 'linkedin', 
                 'photo_url', 'type', 'achievements', 'specialties', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProgramPersonSerializer(serializers.ModelSerializer):
    program = serializers.StringRelatedField()
    person = serializers.StringRelatedField()
    
    class Meta:
        model = ProgramPerson
        fields = ['id', 'program', 'person', 'created_at']
        read_only_fields = ['id', 'created_at']


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = News
        fields = ['id', 'title', 'excerpt', 'content', 'category', 'author', 
                 'featured', 'published_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'published_at', 'created_at', 'updated_at']