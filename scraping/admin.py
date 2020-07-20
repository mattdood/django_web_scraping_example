from django.contrib import admin

# Register your models here.
from .models import News

class NewsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("News", {"fields": ["title", "link", "published"]}),
        ("DB Dates", {"fields": ["created_at, updated_at"]}),
        ("Source", {"fields": ["source"]}),
    ]


admin.site.register(News, NewsAdmin)