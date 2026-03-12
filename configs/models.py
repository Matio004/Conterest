from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


# Create your models here.
class Config(models.Model):
    STATUS_CHOICES = (
        ('private', 'Private'),
        ('published', 'Published'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='configs_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='created')
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')

    description = models.TextField(blank=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='private')

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)

    class Meta:
        ordering = ('-created',)
        constraints = [
            models.UniqueConstraint(fields=['user', 'slug'], name='unique_slug_per_user')
        ]

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    def get_absolute_url(self):  # todo
        return reverse('posts:post_detail', args=[self.user.username,
                                                  self.created.year,
                                                  self.created.strftime('%m'),
                                                  self.created.strftime('%d'),
                                                  self.slug])



# class Image(models.Model):
#     config = models.ForeignKey(Config, on_delete=models.CASCADE, related_name='config_images')
#     image = models.ImageField(upload_to='images/%Y/%m/%d')


class Comment(models.Model):
    config = models.ForeignKey(Config, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comment_created',
                             on_delete=models.CASCADE)

    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment added by {self.user.username} for {self.config.title}'