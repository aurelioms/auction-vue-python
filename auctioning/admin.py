from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Question, Product, Rquestion

admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'proimage', 'birth']
    ordering = ['email']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['time', 'sender', 'recip', 'text', 'public']
    ordering = ['time']


@admin.register(Product)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image', 'description','bidend']
    ordering = ['title']

@admin.register(Rquestion)
class rquestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'productid']
    ordering = ['productid']
