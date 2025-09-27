from django.shortcuts import render, redirect
from .models import Room, Booking
from .forms import BookingForm
from django.contrib import messages

def home(request):
    rooms = Room.objects.all()
    return render(request, "home.html", {"rooms": rooms})


def book_room(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data["room"]
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            
            overlap = Booking.objects.filter(
                room=room,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()

            if overlap:
                messages.error(request, "Ця кімната вже зайнята на вибрані дати.")
            else:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()
                messages.success(request, "Бронювання успішно створене!")
                return redirect("home")
    else:
        form = BookingForm()
    return render(request, "book_room.html", {"form": form})
