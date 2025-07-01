# twccapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe

class SliderImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='slider_images/')
    caption = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title
        
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="150" />')
    image_tag.short_description = 'Image Preview'



class Subscriber(models.Model):
    subscriber = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscriber

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    join_date = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(upload_to='members/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.business_name}"

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, default='fas fa-cog')

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)

    def get_embed_url(self):
        # Convert YouTube URL to embed format
        video_id = self.youtube_url.split('v=')[1]
        if '&' in video_id:
            video_id = video_id.split('&')[0]
        return f"https://www.youtube.com/embed/{video_id}"

    def __str__(self):
        return self.title