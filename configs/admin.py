from django.contrib import admin

from .models import Config, Comment

# Register your models here.
@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'slug', 'url', 'image', 'description', 'publish', 'status']
    prepopulated_fields = {'slug': ('title',)}


# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ['config', 'image']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['config', 'user', 'body', 'created', 'updated']