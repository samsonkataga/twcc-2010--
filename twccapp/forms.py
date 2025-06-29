# twccapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member, ContactMessage, Subscriber
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'youtube_url', 'description', 'thumbnail']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['subscriber']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message']
    

class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['business_name', 'business_type', 'registration_number', 
                 'phone_number', 'address', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
