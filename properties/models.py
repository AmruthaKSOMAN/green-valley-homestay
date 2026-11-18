from django.db import models
from django.core.validators import MinValueValidator


class Property(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    description = models.TextField()

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )

    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(blank=True)

    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)

    whole_building_price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name


class Room(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    name = models.CharField(max_length=150)
    room_number = models.CharField(max_length=20)

    slug = models.SlugField(blank=True, null=True)

    description = models.TextField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    max_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    bed_count = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

        constraints = [
            models.UniqueConstraint(
                fields=["property", "room_number"],
                name="unique_room_number_per_property"
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.room_number}"


class RoomImage(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="rooms/")

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    is_primary = models.BooleanField(default=False)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Room Image"
        verbose_name_plural = "Room Images"
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"Image for {self.room.name}"
