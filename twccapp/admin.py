# twccapp/admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe 
from .models import Member, NewsletterPDF, CompanyProfile, Advertisement, Newsletter, Partner, Project, News, Leadership, Services, FAQ, ContactMessage, Subscriber,SliderImage, VideoUpdate, Publication, GalleryImage

@admin.register(NewsletterPDF)
class NewsletterPDFAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    readonly_fields = ('updated_at',)



@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'uploaded_at')  # Fields to display in the admin list view
    list_filter = ('is_active', 'uploaded_at')            # Add filters for these fields
    search_fields = ('title',)                           # Enable search by title
    date_hierarchy = 'uploaded_at'  




@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published')
    list_filter = ('is_published',)
    actions = ['send_to_subscribers']
    
    def send_to_subscribers(self, request, queryset):
        for newsletter in queryset:
            if newsletter.is_published and newsletter.pdf_file:
                newsletter.send_to_subscribers = True
                newsletter.save()
        self.message_user(request, "Selected newsletters will be sent to subscribers")
    send_to_subscribers.short_description = "Send to subscribers"

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)


# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('title', 'is_active', 'created_at')
#     list_filter = ('is_active',)
#     search_fields = ('title', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    search_fields = ('title', 'content', 'summary')
    list_filter = ('date_posted', 'author')
    
    def save_model(self, request, obj, form, change):
        if not obj.author:  # Set author if empty
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set author if creating new project
            obj.author = request.user
        super().save_model(request, obj, form, change)

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

admin.site.register(Services)
admin.site.register(FAQ)
admin.site.register(ContactMessage)
admin.site.register(Subscriber)


@admin.register(VideoUpdate)
class VideoUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'date_posted', 'is_active')
    list_filter = ('is_active', 'date_posted')
    search_fields = ('title', 'video_url')
    list_editable = ('is_active',)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_article')
    list_filter = ('is_article', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set author during creation
            obj.author = request.user
        super().save_model(request, obj, form, change)

# class GalleryImageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'uploaded_by', 'uploaded_at')
#     list_filter = ('uploaded_at',)
#     search_fields = ('title', 'description')
#     readonly_fields = ('uploaded_at',)
    
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:  # Only set uploaded_by during creation
#             obj.uploaded_by = request.user
#         super().save_model(request, obj, form, change)

admin.site.register(Publication, PublicationAdmin)
# admin.site.register(GalleryImage, GalleryImageAdmin)

@admin.register(Leadership)  # Preferred modern syntax
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active', 'image_tag')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position')
    readonly_fields = ('image_tag',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'position', 'bio', 'image', 'image_tag', 'order', 'is_active')
        }),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'order')
    list_editable = ('order',)
    
    def logo_preview(self, obj):
        return mark_safe(f'<img src="{obj.logo.url}" style="max-height: 50px;" />')
    logo_preview.short_description = 'Logo Preview'



# @admin.register(GalleryImage)
# class GalleryImageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'uploaded_by', 'uploaded_at')
#     readonly_fields = ('uploaded_at',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'content', 'summary')
    list_filter = ('uploaded_at', 'uploaded_by')
    
    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:  # Set uploaded_by if empty
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)