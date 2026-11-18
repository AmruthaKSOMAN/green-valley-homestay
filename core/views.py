
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from properties.models import Room
from bookings.models import Booking

# Public Home Page

def home(request):

    rooms = Room.objects.filter(
        is_active=True,
        property__is_active=True
    ).prefetch_related('images').order_by('id')

    for room in rooms:
        room_images = list(room.images.all())

        room.display_image = next(
            (image for image in room_images if image.is_primary),
            room_images[0] if room_images else None
        )

    context = {
        'rooms': rooms
    }

    return render(request, 'core/home.html', context)


# Owner Dashboard
@login_required
def dashboard(request):

    bookings = Booking.objects.select_related(
        'property',
        'room'
    ).order_by('-created_at')

    context = {
        'bookings': bookings,
    }

    return render(
        request,
        'core/dashboard.html',
        context
    )
