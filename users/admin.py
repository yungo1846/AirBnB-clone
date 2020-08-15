from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models  # .이 의미 하는 것은 같은 현재 py파일인 admin.py와 같은 위치의 폴더를 의미
from rooms import models as room_models


class RoomInline(admin.TabularInline):
    model = room_models.Room


# Register your models here.
@admin.register(models.User)  # 데코레이터는 클래스 바로 위에 위치해야 제대로 동작한다.
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profiles",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "language",
                    "birthdate",
                    "currency",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)
