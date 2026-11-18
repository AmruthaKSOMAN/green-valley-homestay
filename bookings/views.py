
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Q

from properties.models import Property
from .models import Booking
from .forms import BookingForm

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def create_booking(request):

    property_obj = Property.objects.filter(
        is_active=True
    ).first()

    if not property_obj:
        messages.error(
            request,
            'Booking is currently unavailable.'
        )
        return redirect('core:home')

    if request.method == 'POST':

        form = BookingForm(request.POST)

        if form.is_valid():

            booking_type = form.cleaned_data['booking_type']
            room = form.cleaned_data['room']
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            # Find overlapping active bookings.
            overlapping_bookings = Booking.objects.filter(
                property=property_obj,
                status__in=['pending', 'confirmed'],
                check_in__lt=check_out,
                check_out__gt=check_in
            )

            if booking_type == 'room':

                overlapping_bookings = overlapping_bookings.filter(
                    Q(booking_type='whole') |
                    Q(booking_type='room', room=room)
                )

                if overlapping_bookings.exists():

                    form.add_error(
                        None,
                        'This room is not available for the selected dates.'
                    )

                else:

                    save_booking(
                        form,
                        property_obj,
                        room,
                        check_in,
                        check_out,
                        request
                    )

                    return redirect('bookings:booking_success')

            else:

                if overlapping_bookings.exists():

                    form.add_error(
                        None,
                        'The building is not available for the selected dates.'
                    )

                else:

                    save_booking(
                        form,
                        property_obj,
                        None,
                        check_in,
                        check_out,
                        request
                    )

                    return redirect('bookings:booking_success')

    else:

        selected_room = request.GET.get('room')

        form = BookingForm(
            initial={
                'booking_type': 'room',
                'room': selected_room,
            }
        )

    return render(
        request,
        'bookings/booking_form.html',
        {'form': form}
    )


def save_booking(form, property_obj, room, check_in, check_out, request):

    booking = form.save(commit=False)

    booking.property = property_obj
    booking.room = room

    booking.total_nights = (check_out - check_in).days

    if booking.booking_type == 'room':

        booking.total_amount = (
            room.price_per_night * booking.total_nights
        )

    else:

        booking.total_amount = (
            property_obj.whole_building_price_per_night
            * booking.total_nights
        )

    booking.status = 'pending'

    booking.save()

    messages.success(
        request,
        'Your booking request has been submitted successfully.'
    )


def booking_success(request):

    return render(
        request,
        'bookings/booking_success.html'
    )


@login_required
def confirm_booking(request, booking_id):

    if request.method == 'POST':

        booking = get_object_or_404(
            Booking,
            id=booking_id
        )

        if booking.status == 'pending':
            booking.status = 'confirmed'
            booking.save()

            messages.success(
                request,
                'Booking confirmed successfully.'
            )

    return redirect('core:dashboard')


@login_required
def cancel_booking(request, booking_id):

    if request.method == 'POST':

        booking = get_object_or_404(
            Booking,
            id=booking_id
        )

        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()

            messages.success(
                request,
                'Booking cancelled successfully.'
            )

    return redirect('core:dashboard')