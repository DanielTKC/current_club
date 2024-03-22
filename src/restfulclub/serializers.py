from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Match, Suite, Reservation, User
from django.db.models import Exists, OuterRef
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_field
import logging

logger = logging.getLogger(__name__)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'address', 'city', 'state', 'zip_code',
                  'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    formatted_match_date = serializers.SerializerMethodField()
    formatted_match_time = serializers.SerializerMethodField()
    available_suites = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'opponent', 'match_date', 'location', 'match_image', 'formatted_match_date',
                  'formatted_match_time', 'available_suites']

    @extend_schema_field(serializers.CharField())
    def get_formatted_match_date(self, obj):
        formatted_date = obj.match_date.strftime("%B %d, %Y")

        return f"{formatted_date}"

    @extend_schema_field(serializers.CharField())
    def get_formatted_match_time(self, obj):

        formatted_time = obj.match_date.strftime(" %I:%M %p")
        return f"{formatted_time}"

    @extend_schema_field(serializers.CharField())
    def get_available_suites(self, obj):

        if self.context.get('include_available_suites', False):
            suites = Suite.objects.annotate(
                is_sold_out=Exists(
                    Reservation.objects.filter(suite=OuterRef('pk'), match=obj)
                )
            ).filter(is_sold_out=False)
            return SuiteSerializer(suites, many=True, context=self.context).data
        else:
            return None


class SuiteSerializer(serializers.HyperlinkedModelSerializer):
    # tickets_available = serializers.SerializerMethodField()
    is_sold_out = serializers.BooleanField(read_only=True, default=False)
    # total_price = serializers.SerializerMethodField()
    available_matches = serializers.SerializerMethodField()

    class Meta:
        model = Suite
        fields = ['id', 'name', 'capacity', 'price', 'suite_photo', 'amenities', 'description',
                  'is_sold_out', 'total_price', 'available_matches']

    def get_tickets_available(self, obj):
        return obj.capacity

    @extend_schema_field(serializers.CharField())
    def get_available_matches(self, obj):
        # check to see if the context was passed
        if self.context.get('include_available_matches', False):
            available_matches = Match.objects.exclude(
                id__in=Reservation.objects.filter(suite=obj).values_list('match_id', flat=True)
            )
            from .serializers import MatchSerializer
            logger.debug(f"Available matches for suite {obj.id}: {[match.id for match in available_matches]}")

            return MatchSerializer(available_matches, many=True, context=self.context).data
        else:
            return None

    # def get_total_price(self, obj):
    #     total_price =  obj.price * obj.capacity
    #     return "{:,.2f}".format(total_price)


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    match_details = MatchSerializer(source='match', read_only=True)
    suite_details = SuiteSerializer(source='suite', read_only=True)
    total_price = serializers.DecimalField(
        max_digits=8, decimal_places=2, read_only=True
    )

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'suite', 'match', 'match_details', 'suite_details', 'reservation_date', 'total_price']

    def create(self, validated_data):
        print(f"Received data in ReservationSerializer: {validated_data}")
        try:
            validated_data['user'] = self.context['request'].user
            suite = validated_data['suite']
            match = validated_data['match']

            if Reservation.objects.filter(suite=suite, match=match).exists():
                raise ValidationError({'error': 'This suite is already booked for the selected match.'})

            validated_data['total_price'] = suite.price * suite.capacity
            return super().create(validated_data)
        except KeyError as e:
            print(f"Missing key in validated_data: {str(e)}")
            raise ValidationError({'error': f'Missing field: {str(e)}'})
        except ValidationError as e:
            print(f"Validation error in ReservationSerializer: {e.detail}")
            raise
        except Exception as e:
            print(f"Error in ReservationSerializer: {str(e)}")
            raise

    def get_total_price(self, obj):
        # Calculate total price based on suite's price and capacity
        total_price = obj.suite.price * obj.suite.capacity
        return f"{total_price:.2f}"
