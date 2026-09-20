from django.contrib import admin
from .models import Category, Item, Profile, Message


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'seller', 'price', 'is_sold', 'created_at')
    list_filter = ('is_sold', 'category', 'created_at')
    search_fields = ('title', 'description', 'seller__username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'item', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('body', 'sender__username', 'receiver__username', 'item__title')
