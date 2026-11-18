
from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        'customer_name',
        'booking_type',
        'room',
        'check_in',
        'check_out',
        'number_of_guests',
        'total_amount',
        'status',
        'created_at',
    )

    list_filter = (
        'booking_type',
        'status',
        'check_in',
        'created_at',
    )

    search_fields = (
        'customer_name',
        'customer_email',
        'customer_phone',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = ('-created_at',)
