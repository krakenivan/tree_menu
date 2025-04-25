from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "menu_name", "parent", "url", "named_url", "order")
    list_filter = ("menu_name",)
    search_fields = ("name", "menu_name", "url", "named_url")
    fields = ("name", "parent", "menu_name", "url", "named_url", "order")
