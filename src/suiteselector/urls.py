from django.urls import path
from .views import indexPageView, matchesPageView, registrationPageView, suitesPageView, \
    displayReservationsPageView, reservationFormView, reservationSuccessView


urlpatterns = [
    path("", indexPageView, name="index"),
    path("matches/", matchesPageView, name="matches"), 
    path("registration/", registrationPageView, name="registration"),
    path("suites/", suitesPageView, name="suites"), 
    # path("reservationForm/", reservationFormPageView, name="reservationForm"),
    path("displayReservations/", displayReservationsPageView, name="displayReservations"),
    path('reservation/<int:match_id>/<int:suite_id>/', reservationFormView, name='reservation_form'),
    path('reservation/success/', reservationSuccessView, name='reservation_success'),


            ]
