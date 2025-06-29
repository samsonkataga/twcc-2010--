# twccapp/admin.py
from django.contrib import admin
from .models import Member, News, Service, FAQ, ContactMessage, Subscriber
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'business_type', 'join_date')
    search_fields = ('user__username', 'business_name')
    list_filter = ('business_type', 'join_date')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    search_fields = ('title', 'content')
    list_filter = ('date_posted',)

admin.site.register(Service)
admin.site.register(FAQ)
admin.site.register(ContactMessage)
admin.site.register(Subscriber)
