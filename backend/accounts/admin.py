from django.contrib import admin

from .models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
