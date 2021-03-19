from django.contrib import admin
from apps.users.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin')

admin.site.register(User, UserAdmin)
