# twccapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member, ContactMessage, Subscriber
from .models import VideoUpdate
from django.contrib.auth.models import User

class VideoUpdateForm(forms.ModelForm):
    class Meta:
        model = VideoUpdate
        fields = ['title', 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'})
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','subject','message']
    

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['business_name', 'business_type', 'registration_number', 
                 'phone_number', 'address', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }