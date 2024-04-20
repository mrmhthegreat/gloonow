from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    list_display = ["email",'first_name','last_name', "email_is_verified",'is_salonowner']
    search_fields = ["email",'first_name','last_name']
    list_filter = ['is_salonowner','email_is_verified','rating']

    ordering = ["email"]
    readonly_fields = ["date_joined",]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                   
                    "password1",
                    "password2",
                     "email_is_verified",'address','company','is_active','is_salonowner','phone_number','profile_image'
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name",  "rating",   "email_is_verified",'address','company','is_salonowner','phone_number','profile_image')}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    