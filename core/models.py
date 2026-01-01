import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

class Profile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('reviewer', 'Reviewer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'profiles'
        indexes = [
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.role})"

class Program(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    description = models.TextField()
    duration = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    category = models.TextField()
    students = models.IntegerField(default=0)
    key_topics = ArrayField(models.TextField(), blank=True, default=list)
    additional_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'programs'
    
    def __str__(self):
        return self.name

class Person(models.Model):
    TYPE_CHOICES = [
        ('faculty', 'Faculty'),
        ('mentor', 'Mentor'),
        ('staff', 'Staff'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    position = models.TextField()
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    achievements = ArrayField(models.TextField(), blank=True, default=list)
    specialties = ArrayField(models.TextField(), blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'people'
    
    def __str__(self):
        return f"{self.name} ({self.position})"

class ProgramPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_people')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_programs')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'program_people'
        unique_together = ['program', 'person']
    
    def __str__(self):
        return f"{self.program.name} - {self.person.name}"

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    excerpt = models.TextField()
    content = models.TextField()
    category = models.TextField()
    author = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'news'
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title