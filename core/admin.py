from django.contrib import admin
from .models import Profile, Program, Person, ProgramPerson, News


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'category', 'students', 'created_at']
    list_filter = ['level', 'category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'type', 'email', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['name', 'position', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(ProgramPerson)
class ProgramPersonAdmin(admin.ModelAdmin):
    list_display = ['program', 'person', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['id', 'created_at']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'featured', 'published_at']
    list_filter = ['category', 'featured', 'published_at']
    search_fields = ['title', 'content']
    readonly_fields = ['id', 'created_at', 'updated_at']