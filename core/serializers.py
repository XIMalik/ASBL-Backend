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
                 'students', 'key_topics', 'additional_details', 'created_at', 'updated_at']
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