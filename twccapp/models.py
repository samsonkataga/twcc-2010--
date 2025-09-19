# twccapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from django.db import models
from django.db.models.signals import post_save  # Add this import
from django.dispatch import receiver  
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class Donation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    donated_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - ${self.amount}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    image = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Upload a profile photo of the person giving the testimonial"
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Testimonial by {self.name}"
    
    class Meta:
        ordering = ['-created_at']


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
    redirect_url = models.URLField(max_length=500, blank=True, null=True, default=None)  # Added URL field
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

class UpcomingEvent(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='upcoming_event/', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title 

# class Services(models.Model):
#     ICON_CHOICES = [
#         ('fa-money-bill-wave', 'Financial (money bill)'),
#         ('fa-handshake', 'Networking (handshake)'),
#         ('fa-chart-line', 'Capacity (growth chart)'),
#         ('fa-bullhorn', 'Advocacy (megaphone)'),
#         ('fa-users', 'Team (users)'),
#         ('fa-globe', 'Global (globe)'),
#         # Add more icons as needed
#     ]

#     title = models.CharField(max_length=200)
#     icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='fa-handshake')
#     content = models.TextField()
#     summary = models.TextField(default=True)
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return self.title 

class Services(models.Model):
    CATEGORY_CHOICES = [
        ('financial_linkage', 'Financial Linkage'),
        ('networking_marketing', 'Networking and Marketing'),
        ('capacity_building', 'Capacity Building'),
        ('advocacy', 'Advocacy'),
        ('market_access', 'Market Access and Digitalization'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=True)
    content = models.TextField()
    summary = models.TextField(default="Service summary")
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


# class Advertisement(models.Model):
#     title = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='advertisements/', blank=True, null=True)
#     url = models.URLField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
#     def __str__(self):
#         return self.title
        
#     class Meta:
#         ordering = ['-created_at']


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
    
    @property
    def is_recent(self):
        """Return True if the ad was created within the last 7 days"""
        return timezone.now() - self.created_at < timedelta(days=2)


class RecentAdvert(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recent_adverts/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='recent_adverts/pdfs/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Recent Advert"
        verbose_name_plural = "Recent Adverts"
    
    @property
    def is_recent(self):
        """Return True if the advert was created within the last 2 days"""
        return timezone.now() - self.created_at < timedelta(days=2)
    
    def get_absolute_url(self):
        if self.pdf_file:
            return self.pdf_file.url
        return self.url if self.url else '#'



# class GalleryImage(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='gallery/')
#     uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     order = models.PositiveIntegerField(default=0)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default='Default content')  # Add default value
    summary = models.TextField(default='Default summary') 
    image = models.ImageField(upload_to='gallery/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-uploaded_at']



class NewsletterPDF(models.Model):
    title = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='newsletters/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(default='Default summary text')  # Added default value
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class YouthWingContent(models.Model):
    hero_image = models.ImageField(upload_to='youth_wing/hero/', blank=True, null=True)
    about_image = models.ImageField(upload_to='youth_wing/about/', blank=True, null=True)
    about_content = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Youth Wing Content"

    class Meta:
        verbose_name = "Youth Wing Content"
        verbose_name_plural = "Youth Wing Content"

class YouthProgram(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='youth_wing/programs/', blank=True, null=True)
    description = models.TextField()
    details = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        

# class YouthLeader(models.Model):
#     name = models.CharField(max_length=100)
#     position = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='youth_wing/leaders/', blank=True, null=True)
#     bio = models.TextField()
#     is_active = models.BooleanField(default=True)
#     order = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"{self.name} - {self.position}"

#     class Meta:
#         ordering = ['order']

class YouthGallery(models.Model):
    image = models.ImageField(upload_to='youth_wing/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.caption if self.caption else f"Gallery Image {self.id}"

    class Meta:
        verbose_name_plural = "Youth Gallery"
        ordering = ['-upload_date']

class Document(models.Model):
    TYPE_CHOICES = [
        ('constitution', 'Constitution'),
        ('strategic_plan', 'Strategic Plan'),
        ('code_of_conduct', 'Code of Conduct'),
    ]
    
    document_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        unique=True,
        help_text="Type of document"
    )
    pdf_file = models.FileField(
        upload_to='documents/',
        help_text="Upload PDF file"
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_document_type_display()

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

class Report(models.Model):
    TYPE_CHOICES = [
        ('annual_report', 'Annual Report'),
        ('research_paper', 'Research Paper & Study'),
        ('strategic_plan', 'Strategic Plan'),
        ('newsletter', 'Newsletter'),
        ('press_release', 'Press Release'),
        ('company_profile', 'Company Profile'),
        # ... (your existing choices)
    ]
    
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200, help_text="Report title (e.g., '2023 Annual Report')")  # New field
    pdf_file = models.FileField(upload_to='report/')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.title}"

    class Meta:
        ordering = ['-updated_at']  # Newest first

class ImpactStory(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='impact_stories/')
    category = models.CharField(max_length=50, choices=[
        ('all', 'All Stories'),
        ('fashion', 'Women in Sustainable Fashion'),
        ('markets', 'Women in Regional Markets'),
        ('youth', 'Youth-Led Innovations'),
        ('agriculture', 'Women in Agriculture'),
        ('other', 'Other Sectors'),
    ])
    featured = models.BooleanField(default=False)
    date_published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Impact Stories"
        ordering = ['-date_published']

class YouthStory(models.Model):
    YOUTH_CATEGORIES = [
        ('success', 'Youth Success Stories'),
        ('involved', 'Get Involved'),
        ('events', 'Events & Activities'),
        ('resources', 'Resources for Youth'),
        ('leadership', 'Leadership Training'),
        ('entrepreneurship', 'Entrepreneurship Bootcamp'),
        ('digital', 'Digital Skills Workshops'),
        ('trade', 'Youth Trade Missions'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to='youth_stories/')
    category = models.CharField(max_length=50, choices=YOUTH_CATEGORIES)
    featured = models.BooleanField(default=False)
    date_published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Youth Stories"
        ordering = ['-date_published']
