from django.contrib import admin
from .models import *

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'date_joined']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'bio']


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['member', 'transaction_type', 'category','describe','price','date']

@admin.register(Category)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'category_name']