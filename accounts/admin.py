from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    ordering = ("id",)

    list_display = (
        "id",
        "email",
        "first_name",
        "is_verified",
        "is_online",
        "is_staff",
    )

    search_fields = (
        "email",
        "first_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_seen",
    )

    fieldsets = (
        (
            "Account",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),

        (
            "Personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone",
                    "bio",
                    "avatar",
                )
            },
        ),

        (
            "Status",
            {
                "fields": (
                    "is_online",
                    "last_seen",
                    "is_verified",
                )
            },
        ),

        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),

        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )