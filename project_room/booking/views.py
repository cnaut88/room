from django.shortcuts import render, redirect
from .models import Room, Booking
from .forms import BookingForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
def home(request):
    rooms = Room.objects.all()
    return render(request, "home.html", {"rooms": rooms})


def login_register(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Невірний логін або пароль")

        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Помилка реєстрації. Спробуйте ще раз.")

    return render(request, 'registration/login_register.html', {
        'login_form': login_form,
        'register_form': register_form
    })

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

