from django.contrib import admin
from .models import ChatContent, ChatTopic

# Register your models here.
admin.site.register(ChatContent)
admin.site.register(ChatTopic)
