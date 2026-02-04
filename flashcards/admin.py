from django.contrib import admin
from .models import CardTopic, FlashCard, PDFDocument

# Register your models here.
admin.site.register(CardTopic)
admin.site.register(FlashCard)
admin.site.register(PDFDocument)
