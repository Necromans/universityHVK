from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ChatMessage, Article


#Регистрируем модель CustomUser в админке
admin.site.register(CustomUser)

#Регистрируем модель ChatMessage в админке
admin.site.register(ChatMessage)

#Регистрируем модель Article в админке
admin.site.register(Article)