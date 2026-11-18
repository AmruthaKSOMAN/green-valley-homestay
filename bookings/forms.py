
import re
from django import forms
from .models import Booking
from properties.models import Room


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'booking_type',
            'room',
            'customer_name',
            'customer_email',
            'customer_phone',
            'check_in',
            'check_out',
            'number_of_guests',
            'special_requests',
        ]

        widgets = {
            'booking_type': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'room': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'customer_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your full name'
                }
            ),

            'customer_email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your email'
                }
            ),

            'customer_phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your phone number'
                }
            ),

            'check_in': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'check_out': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'number_of_guests': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1
                }
            ),

            'special_requests': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Any special requests?'
                }
            ),
        }

        labels = {
            'booking_type': 'Booking Type',
            'room': 'Select Room',
            'customer_name': 'Full Name',
            'customer_email': 'Email Address',
            'customer_phone': 'Phone Number',
            'check_in': 'Check-in Date',
            'check_out': 'Check-out Date',
            'number_of_guests': 'Number of Guests',
            'special_requests': 'Special Requests',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['room'].queryset = Room.objects.filter(
            is_active=True,
            property__is_active=True
        ).order_by('id')

        self.fields['room'].required = False

    def clean_customer_phone(self):

        phone = self.cleaned_data.get('customer_phone', '').strip()

        # Allow digits, spaces, hyphens, parentheses
        # and an optional + at the beginning.
        if not re.fullmatch(r'\+?[0-9\s()-]+', phone):

            raise forms.ValidationError(
                'Please enter a valid phone number.'
            )

        # Count only digits.
        digits = re.sub(r'\D', '', phone)

        if len(digits) < 10 or len(digits) > 15:

            raise forms.ValidationError(
                'Phone number must contain between 10 and 15 digits.'
            )

        return phone

    def clean(self):

        cleaned_data = super().clean()

        booking_type = cleaned_data.get('booking_type')
        room = cleaned_data.get('room')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        number_of_guests = cleaned_data.get('number_of_guests')

        if booking_type == 'room' and not room:
            self.add_error(
                'room',
                'Please select a room.'
            )

        if booking_type == 'whole':
            cleaned_data['room'] = None

        if check_in and check_out:

            if check_out <= check_in:
                self.add_error(
                    'check_out',
                    'Check-out date must be after the check-in date.'
                )

        if (
            booking_type == 'room'
            and room
            and number_of_guests
            and number_of_guests > room.max_guests
        ):
            self.add_error(
                'number_of_guests',
                f'This room can accommodate a maximum of {room.max_guests} guests.'
            )

        return cleaned_data
