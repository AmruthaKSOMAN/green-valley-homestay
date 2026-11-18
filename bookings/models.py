
from django.db import models
from django.core.validators import MinValueValidator
from properties.models import Property, Room


class Booking(models.Model):

    BOOKING_TYPE_CHOICES = [
        ('room', 'Individual Room'),
        ('whole', 'Whole Building'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_type = models.CharField(
        max_length=10,
        choices=BOOKING_TYPE_CHOICES,
        default='room'
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )

    customer_name = models.CharField(max_length=150)

    customer_email = models.EmailField()

    customer_phone = models.CharField(max_length=15)

    check_in = models.DateField()

    check_out = models.DateField()

    number_of_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    total_nights = models.PositiveIntegerField(default=0)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    special_requests = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.booking_type}"
