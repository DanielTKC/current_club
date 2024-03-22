from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.views import View
from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
from .models import Match, Suite, Reservation, User
from .serializers import MatchSerializer, SuiteSerializer, ReservationSerializer, UserSerializer


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in
                    self.permission_classes_by_action.get('default', [permissions.IsAuthenticated])]


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'update': [permissions.IsAuthenticated],
                                    'partial_update': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated],
                                    'list': [permissions.IsAuthenticated],
                                    'retrieve': [permissions.IsAuthenticated],
                                    'default': [permissions.IsAuthenticated]}


class MatchViewSet(BaseViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes_by_action = {'create': [permissions.IsAuthenticated],
                                    'update': [permissions.IsAuthenticated],
                                    'partial_update': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated],
                                    'list': [permissions.IsAuthenticatedOrReadOnly],
                                    'retrieve': [permissions.IsAuthenticatedOrReadOnly],
                                    'default': [permissions.IsAuthenticated]}

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned matches to those available for a given suite,
    #     by filtering against a `suiteId` query parameter in the URL.
    #     """
    #     queryset = Match.objects.all()
    #     suite_id = self.request.query_params.get('suiteId', None)
    #     if suite_id is not None:
    #         # Exclude matches that have a reservation for the specified suite
    #         reserved_match_ids = Reservation.objects.filter(suite_id=suite_id).values_list('match_id', flat=True)
    #         queryset = queryset.exclude(id__in=reserved_match_ids)
    #     return queryset

    # this function determines if it is just a match call or a match/{match.id} call
    def get_serializer_context(self):
        context = super(MatchViewSet, self).get_serializer_context()
        context['include_available_suites'] = self.action == 'retrieve'
        return context


class SuiteViewSet(BaseViewSet):
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer
    permission_classes_by_action = {'create': [permissions.IsAuthenticated],
                                    'update': [permissions.IsAuthenticated],
                                    'partial_update': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated],
                                    'list': [permissions.AllowAny],
                                    'retrieve': [permissions.IsAuthenticatedOrReadOnly],
                                    'default': [permissions.IsAuthenticated]}

    def get_serializer_context(self):
        context = super(SuiteViewSet, self).get_serializer_context()
        # Always include available matches in the context for the 'retrieve' action
        context['include_available_matches'] = self.action == 'retrieve'
        return context


class ReservationViewSet(BaseViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes_by_action = {'create': [permissions.IsAuthenticated],
                                    'update': [permissions.IsAuthenticated],
                                    'partial_update': [permissions.IsAuthenticated],
                                    'destroy': [permissions.IsAuthenticated],
                                    'list': [permissions.IsAuthenticated],
                                    'retrieve': [permissions.IsAuthenticated],
                                    'default': [permissions.IsAuthenticated]}

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset


# How we check for authentication

class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "User is logged in."})


# Here's our auth token class
class CustomAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)  # Log the user in to create a session
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        logout(request)
        return HttpResponseRedirect('/')
