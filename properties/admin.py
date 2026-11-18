from django.contrib import admin
from .models import Property, Room, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "city",
        "state",
        "whole_building_price_per_night",
        "is_active",
    )

    list_filter = ("is_active", "city", "state")

    search_fields = ("name", "city", "address")

    prepopulated_fields = {"slug": ("name",)}

    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "room_number",
        "property",
        "price_per_night",
        "max_guests",
        "is_active",
    )

    list_filter = ("is_active", "property")

    search_fields = ("name", "room_number")

    inlines = [RoomImageInline]


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):

    list_display = (
        "room",
        "caption",
        "is_primary",
        "display_order",
    )

    list_filter = ("is_primary",)

    search_fields = ("room__name", "caption")
