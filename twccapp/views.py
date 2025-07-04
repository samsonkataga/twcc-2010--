# twccapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User  # Add this import
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import News, Service, FAQ, ContactMessage, Partner, Leadership, VideoUpdate, SliderImage, Publication, GalleryImage
from django.contrib.auth.decorators import login_required
from .forms import MemberRegistrationForm, CustomUserCreationForm, ContactForm, SubscribeForm, VideoUpdateForm 



def publications_list(request):
    articles = Publication.objects.filter(is_article=True).order_by('-created_at')
    documentations = Publication.objects.filter(is_article=False).order_by('-created_at')
    return render(request, 'twccapp/publications_list.html', {
        'articles': articles,
        'documentations': documentations
    })

def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'twccapp/publication_detail.html', {'publication': publication})

def gallery_view(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'twccapp/gallery.html', {'images': images})

# def index(request):
#     latest_news = News.objects.all().order_by('-date_posted')[:3]
#     slider_images = SliderImage.objects.filter(is_active=True).order_by('order')
#     videos = VideoUpdate.objects.filter(is_active=True).order_by('-date_posted')[:6]
    
#     # Handle video form submission if it's a POST request
#     if request.method == 'POST' and 'video_url' in request.POST and is_admin(request.user):
#         form = VideoUpdateForm(request.POST)
#         if form.is_valid():
#             video = form.save(commit=False)
#             video.posted_by = request.user
#             video.save()
#             messages.success(request, 'Video added successfully!')
#             return redirect('index')
#     else:
#         form = VideoUpdateForm()
    
#     context = {
#         'latest_news': latest_news,
#         'slider_images': slider_images,
#         'videos': videos,
#         'video_form': form
#     }
#     return render(request, 'twccapp/index.html', context)



def index(request):
    latest_news = News.objects.all().order_by('-date_posted')[:3]
    slider_images = SliderImage.objects.filter(is_active=True).order_by('order')
    
    context = {
        'latest_news': latest_news,
        'slider_images': slider_images,
    }
    return render(request, 'twccapp/index.html', context)

def about(request):
    leaders = Leadership.objects.filter(is_active=True).order_by('order')[:6]
    return render(request, 'twccapp/about.html', {'leaders': leaders})

def services(request):
    services = Service.objects.all()
    partners = Partner.objects.all().order_by('order')
    context = {
        'services': services,
        'partners': partners
    }
    return render(request, 'twccapp/services.html', context)

def news(request):
    news_list = News.objects.all().order_by('-date_posted')
    videos = VideoUpdate.objects.filter(is_active=True).order_by('-date_posted')[:6]
    
    # Handle video form submission if it's a POST request
    if request.method == 'POST' and 'video_url' in request.POST and is_admin(request.user):
        form = VideoUpdateForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.posted_by = request.user
            video.save()
            messages.success(request, 'Video added successfully!')
            return redirect('news')
    else:
        form = VideoUpdateForm()
    
    context = {
        'news_list': news_list,
        'videos': videos,
        'video_form': form
    }
    return render(request, 'twccapp/news.html', context)

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

# def register(request):
#     if request.method == 'POST':
#         user_form = CustomUserCreationForm(request.POST)
#         member_form = MemberRegistrationForm(request.POST, request.FILES)
        
#         if user_form.is_valid() and member_form.is_valid():
#             # Save user first
#             user = user_form.save()
            
#             # Save member with user reference
#             member = member_form.save(commit=False)
#             member.user = user  # This connects the Member to the User
#             member.save()  # Now both user and member are saved
#             messages.success(request, 'Registration successful! Welcome to our site.')
#             return redirect('login')
            
#             # Login the user
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             # Print form errors for debugging
#             print("User form errors:", user_form.errors)
#             print("Member form errors:", member_form.errors)
#     else:
#         user_form = CustomUserCreationForm()
#         member_form = MemberRegistrationForm()
    
#     return render(request, 'twccapp/register.html', {
#         'user_form': user_form,
#         'member_form': member_form
#     })


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        member_form = MemberRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and member_form.is_valid():
            # Check if user already exists
            if User.objects.filter(username=user_form.cleaned_data['username']).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            
            if User.objects.filter(email=user_form.cleaned_data['email']).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')
            
            # Save user first
            user = user_form.save()
            
            # Check if member profile already exists (shouldn't happen, but just in case)
            if not hasattr(user, 'member'):
                # Save member with user reference
                member = member_form.save(commit=False)
                member.user = user
                member.save()
                
                messages.success(request, 'Registration successful! Welcome to our site.')
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Profile already exists for this user')
                return redirect('login')
        else:
            # Print form errors for debugging
            print("User form errors:", user_form.errors)
            print("Member form errors:", member_form.errors)
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
            messages.success(request, 'Login successful! Welcome back!')
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'twccapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

# def dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     return render(request, 'twccapp/dashboard.html')

@login_required
def dashboard(request):
    try:
        member = request.user.member
    except Member.DoesNotExist:
        messages.warning(request, "Please complete your member profile")
        return redirect('complete_profile')
    
    # Calculate profile completion percentage
    required_fields = ['profile_picture', 'business_name', 'business_type', 
                     'registration_number', 'phone_number', 'address']
    completed = sum(1 for field in required_fields if getattr(member, field))
    profile_completion = int((completed / len(required_fields)) * 100)
    
    context = {
        'member': member,
        'profile_completion': profile_completion,
        'upcoming_events': Event.objects.filter(attendees=request.user, start_date__gte=timezone.now()),
        'unread_notifications': Notification.objects.filter(user=request.user, read=False),
        'recent_activities': Activity.objects.filter(user=request.user).order_by('-timestamp')[:5]
    }
    return render(request, 'twccapp/dashboard.html', context)


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing!')
            return redirect('index')  # Redirect back to the same page
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



