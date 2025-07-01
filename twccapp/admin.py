# twccapp/admin.py
from django.contrib import admin
from .models import Member, News, Service, FAQ, ContactMessage, Subscriber,SliderImage, VideoUpdate


class SliderImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'order', 'is_active', 'image_tag')
    list_editable = ('order', 'is_active')
    
admin.site.register(SliderImage, SliderImageAdmin)

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


@admin.register(VideoUpdate)
class VideoUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'date_posted', 'is_active')
    list_filter = ('is_active', 'date_posted')
    search_fields = ('title', 'video_url')
    list_editable = ('is_active',)