import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

from django.http import JsonResponse

from django.template import context


def indexPageView(request):
    return render(request, "suiteselector/index.html")


def matchesPageView(request):
    suite_id = request.GET.get("suiteId")
    context = {}

    if suite_id:
        response = requests.get(f'http://127.0.0.1:8000/api/suites/{suite_id}/')
        data = response.json()
        matches = data.get('available_matches', [])
        context['suite_id'] = suite_id
    else:
        response = requests.get('http://127.0.0.1:8000/api/matches/')
        matches = response.json()
    context['matches'] = matches
    return render(request, 'suiteselector/matches.html', context)


def suitesPageView(request):
    match_id = request.GET.get('matchId')
    context = {}

    if match_id:
        response = requests.get(f'http://127.0.0.1:8000/api/matches/{match_id}/')
        data = response.json()
        suites = data.get('available_suites', [])
        context['match_id'] = match_id
    else:
        response = requests.get('http://127.0.0.1:8000/api/suites/')
        suites = response.json()
    context['suites'] = suites
    return render(request, 'suiteselector/suites.html', context)


def registrationPageView(request):
    return render(request, "suiteselector/registration.html")


def displayReservationsPageView(request):
    context = {}
    response = requests.get('http://127.0.0.1:8000/api/reservations/')
    reservations = response.json()
    context['reservations'] = reservations
    return render(request, 'suiteselector/displayReservations.html', context)


@login_required
def reservationFormView(request, match_id, suite_id):
    user = request.user
    match = requests.get(f'http://127.0.0.1:8000/api/matches/{match_id}/').json()
    suite = requests.get(f'http://127.0.0.1:8000/api/suites/{suite_id}/').json()
    total_price = suite['price'] * suite['capacity']

    context = {
        'user': user,
        'match': match,
        'suite': suite,
        'total_price': total_price,
    }

    if request.method == 'POST':
        # Retrieve form data
        print(f"Form data: {request.POST}")
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')

        # Retrieve the token from the request data
        token = request.POST.get('token')

        # Make an API call to create the reservation
        reservation_data = {
            'match': f'http://127.0.0.1:8000/api/matches/{match_id}/',
            'suite': f'http://127.0.0.1:8000/api/suites/{suite_id}/',
            # Include any additional fields required for the reservation
        }
        headers = {
            'Authorization': f'Token {token}',
        }
        response = requests.post('http://127.0.0.1:8000/api/reservations/', data=reservation_data, headers=headers)

        if response.status_code == 201:
            # Reservation created successfully
            return redirect('reservation_success')
        else:
            # Handle reservation creation failure
            print(f"API response content: {response.content}")
            context['error_message'] = 'Failed to create reservation. Please try again.'
            return render(request, 'suiteselector/reservationForm.html', context)

    return render(request, 'suiteselector/reservationForm.html', context)


@login_required
def reservationSuccessView(request):
    user = request.user
    # Retrieve the token from the user's authentication information
    token = user.auth_token.key
    headers = {
        'Authorization': f'Token {token}',
    }
    response = requests.get(f'http://127.0.0.1:8000/api/reservations/?user={user.id}', headers=headers)
    if response.status_code == 200:
        reservations = response.json()
    else:
        reservations = []
    context = {
        'reservations': reservations,
    }
    return render(request, 'suiteselector/reservationSuccess.html', context)
