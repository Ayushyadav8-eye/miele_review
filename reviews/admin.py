
from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "mobile_number",
        "rating",
        "created_at",
    )

    list_filter = ("rating", "created_at")
    search_fields = ("name", "mobile_number", "comment")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 25
