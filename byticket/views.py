import io
from time import gmtime, strftime
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from byticket.forms import LoginForm, RegistrationForm
from byticket.models import CustomUser, Movie, Category, PurchasedTicket, Cinema, Screening


def welcome_request(request: HttpResponse):
    return render(request, 'byticket/welcome.html')


@login_required
def reservation_success_request(request: HttpResponse):
    return render(request, 'byticket/reservation_success.html')


@login_required
def reservation_failed_request(request: HttpResponse):
    return render(request, 'byticket/reservation_failed.html')


def logout_request(request):
    logout(request)
    return redirect("/welcome")


def login_request(request: HttpResponse):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            messages.debug(request, f'Username: {username}, Password: {password}')
            try:
                user = CustomUser.objects.get(username=username)
                messages.debug(request, f'User from DB: {user}')
                if user is not None:
                    if user.password == password:
                        login(request, user)
                        return redirect('/movies')
                    else:
                        messages.error(request, 'Invalid login or password.')
                else:
                    messages.error(request, 'User does not exist.')

            except CustomUser.DoesNotExist:
                messages.error(request, 'User does not exist')
    else:
        form = LoginForm()

    return render(request, 'byticket/login.html', {'form': form})


def register_request(request: HttpResponse):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.info(request, 'Form is valid.')

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            created_at = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            if password1 == password2:
                user = CustomUser.objects.create(username=username, email=email, password=password1,
                                                 created_at=created_at)
                user.save()
                messages.success(request, f'User created: {user}')
            else:
                messages.info(request, 'Both passwords are not matching.')
                return redirect('/register')

            return redirect('/login')
    else:
        form = RegistrationForm()

    return render(request, 'byticket/register.html', {'form': form})


@login_required
def movies_list_request(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    return render(request, 'byticket/movies_list.html', {'movies': movies, 'categories': categories})


@login_required
def movie_detail_request(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    screenings = Screening.objects.filter(movie=movie)
    return render(request, 'byticket/movie_detail.html', {'movie': movie, 'screenings': screenings})


@login_required
def cinema_detail_request(request, cinema_id):
    cinema = Cinema.objects.get(pk=cinema_id)
    screenings = Screening.objects.filter(cinema=cinema)
    return render(request, 'byticket/cinema_detail.html', {'cinema': cinema, 'screenings': screenings})


@login_required
def screening_detail_request(request, screening_id):
    screening = Screening.objects.get(pk=screening_id)
    seats_count = range(1, screening.seats_count + 1)
    return render(request, 'byticket/screening_detail.html', {'screening': screening, 'seats_count': seats_count})


@login_required
def movies_by_category_request(request, category_id):
    movies = Movie.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    selected_category = Category.objects.get(id=category_id)
    return render(request, 'byticket/movies_list.html', {'movies': movies, 'categories': categories, 'selected_category': selected_category})


@login_required
def profile_request(request):
    user = request.user
    tickets = PurchasedTicket.objects.filter(user=user)
    return render(request, 'byticket/profile.html', {'user': user, 'tickets': tickets})


@login_required
def cinemas_list_request(request):
    cinemas = Cinema.objects.all()
    return render(request, 'byticket/cinemas_list.html', {'cinemas': cinemas})


@login_required
def reserve_seats_request(request):
    if request.method == 'GET':
        seat_data = request.GET.get('seats')
        screening_id = request.GET.get('screening_id')
        if seat_data:
            seat_numbers = seat_data.split(',')
            user = request.user
            screening = Screening.objects.get(pk=screening_id)
            purchase_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            for seat_number in seat_numbers:
                ticket = PurchasedTicket.objects.create(user=user, screening=screening,
                                                        seat_number=seat_number, purchase_time=purchase_time)
                ticket.save()

            return redirect('/reservation/success')

    return redirect('/reservation/failed')


@login_required
def ticket_pdf_request(request, ticket_id):
    ticket = PurchasedTicket.objects.get(pk=ticket_id)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    text_object = c.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont('Helvetica', 20)

    ticket_info_lines = [
        f'Ticket #{ticket.id}',
        '',
        f'Movie: {ticket.screening.movie.title}',
        f'Seat number: {ticket.seat_number}',
        '',
        f'Purchase time: {str(ticket.purchase_time)[0:19]}',
        f'Start time: {str(ticket.screening.start_time)[0:19]}',
        f'Price: {ticket.screening.price} BYN'
    ]

    for line in ticket_info_lines:
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'ticket_{ticket.id}.pdf')


@login_required
def ticket_delete_request(request, ticket_id):
    PurchasedTicket.objects.get(pk=ticket_id).delete()
    return redirect('/profile')


def get_purchased_tickets(request, screening_id):
    purchased_tickets = PurchasedTicket.objects.filter(screening_id=screening_id).values('seat_number')
    return JsonResponse(list(purchased_tickets), safe=False)
