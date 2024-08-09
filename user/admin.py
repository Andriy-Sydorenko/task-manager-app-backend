from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from user.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "nickname", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "nickname", "password", "is_active", "is_staff", "is_superuser")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "email",
        "nickname",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = (
        "email",
        "nickname",
    )
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "nickname", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "nickname", "password1", "password2"),
            },
        ),
    )
