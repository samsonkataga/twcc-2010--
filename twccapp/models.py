# twccapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from django.db import models
from django.db.models.signals import post_save  # Add this import
from django.dispatch import receiver  
from django.core.validators import FileExtensionValidator



class CompanyProfile(models.Model):
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='company_profiles/')
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='slider_images/')
    caption = models.CharField(max_length=755, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title
        
    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" />')
    image_tag.short_description = 'Image Preview'



class Subscriber(models.Model):
    email = models.EmailField(unique=True) 
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

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

    @receiver(post_save, sender=User)
    def create_member_profile(sender, instance, created, **kwargs):
        if created:
            Member.objects.create(user=instance)

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title 

class Services(models.Model):
    ICON_CHOICES = [
        ('fa-money-bill-wave', 'Financial (money bill)'),
        ('fa-handshake', 'Networking (handshake)'),
        ('fa-chart-line', 'Capacity (growth chart)'),
        ('fa-bullhorn', 'Advocacy (megaphone)'),
        ('fa-users', 'Team (users)'),
        ('fa-globe', 'Global (globe)'),
        # Add more icons as needed
    ]

    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fa-handshake')
    content = models.TextField()
    summary = models.TextField(default=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title 

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


class Publication(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    document = models.FileField(upload_to='publications/documents/', blank=True, null=True)
    is_article = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('publication_detail', kwargs={'pk': self.pk})

# class GalleryImage(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='gallery/images/')
#     description = models.TextField(blank=True)
#     uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     uploaded_at = models.DateTimeField(auto_now_add=True) # Changed from auto_now_add
    
#     def __str__(self):
#         return self.title

# class Leadership(models.Model):
#     name = models.CharField(max_length=100)
#     position = models.CharField(max_length=100)
#     bio = models.TextField()
#     image = models.ImageField(upload_to='leadership/')
#     order = models.PositiveIntegerField(default=0)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name_plural = "Leadership Team"
#         ordering = ['order']

#     def __str__(self):
#         return f"{self.name} - {self.position}"

#     def image_tag(self):
#         if self.image:
#             return mark_safe(f'<img src="{self.image.url}" width="50" />')
#         return "No Image"
#     image_tag.short_description = 'Image Preview'



class Leadership(models.Model):
    CATEGORY_CHOICES = [
        ('board', 'Board of Directors'),
        ('leadership', 'Leadership Team'),
        ('staff', 'Staff Members'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='leadership/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='staff')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Leadership Team"
        ordering = ['category', 'order']

    def __str__(self):
        return f"{self.name} - {self.position}"

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50" />')
        return "No Image"
    image_tag.short_description = 'Image Preview'



class Partner(models.Model):
    logo = models.ImageField(upload_to='partners/')
    order = models.PositiveIntegerField(default=0)  # For manual ordering
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Partners'

    def __str__(self):
        return f"Partner #{self.id}"



class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(
        upload_to='newsletters/',
        validators=[FileExtensionValidator(['pdf'])],
        help_text='Upload PDF newsletter'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    send_to_subscribers = models.BooleanField(default=False, 
        help_text='Send to all subscribers when published')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Advertisement(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='advertisements/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_at']




class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title