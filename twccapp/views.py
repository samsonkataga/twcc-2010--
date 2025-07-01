# twccapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import News, Service, FAQ, ContactMessage, Video, SliderImage
from django.contrib.auth.decorators import login_required
from .forms import MemberRegistrationForm, CustomUserCreationForm, ContactForm, SubscribeForm, VideoForm 



def index(request):
    latest_news = News.objects.all().order_by('-date_posted')[:3]
    slider_images = SliderImage.objects.filter(is_active=True).order_by('order')
    context = {
        'latest_news': latest_news,
        'slider_images': slider_images,
    }
    return render(request, 'twccapp/index.html', context)

def about(request):
    return render(request, 'twccapp/about.html')

def services(request):
    services = Service.objects.all()
    return render(request, 'twccapp/services.html', {'services': services})

def news(request):
    news_list = News.objects.all().order_by('-date_posted')
    return render(request, 'twccapp/news.html', {'news_list': news_list})

def news_detail(request, pk):
    news_item = News.objects.get(pk=pk)
    return render(request, 'twccapp/news_detail.html', {'news_item': news_item})

def faqs(request):
    faqs = FAQ.objects.all()
    return render(request, 'twccapp/faqs.html', {'faqs': faqs})

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Now this will work
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')  # PRG pattern
    else:
        form = ContactForm()


    
    return render(request, 'twccapp/contact.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        member_form = MemberRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and member_form.is_valid():
            user = user_form.save()
            member = member_form.save(commit=False)
            member.user = user
            member.save()
            login(request, user)
            return redirect('dashboard')  # Make sure you have this URL defined
    else:
        user_form = CustomUserCreationForm()
        member_form = MemberRegistrationForm()
    
    return render(request, 'twccapp/register.html', {
        'user_form': user_form,
        'member_form': member_form
    })



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'twccapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'twccapp/dashboard.html')


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('subscribe')  # Redirect back to the same page
    else:
        form = SubscribeForm()
    
    return render(request, 'twccapp/subscribe.html', {'form': form})


def video_list(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'twccapp/videos_list.html', {'videos': videos})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'twccapp/videos_detail.html', {'video': video})

@login_required
def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'twccapp/videos_upload.html', {'form': form})