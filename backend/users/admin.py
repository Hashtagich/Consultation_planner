from django.contrib import admin
from .models import User, Role


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'role')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
