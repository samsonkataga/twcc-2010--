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


class VideoUpdate(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    embed_code = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Convert YouTube URL to embed code if needed
        if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
            video_id = self.extract_youtube_id(self.video_url)
            self.embed_code = f'<iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        super().save(*args, **kwargs)

    @staticmethod
    def extract_youtube_id(url):
        # Extract YouTube ID from various URL formats
        import re
        pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(pattern, url)
        return match.group(1) if match else None

    def __str__(self):
        return self.title