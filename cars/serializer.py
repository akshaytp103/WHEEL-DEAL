
from rest_framework import serializers
from .models import *
from django.utils import timezone
from datetime import date, datetime

from cars.models import *
# from car.serializers import CarSerializer 
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


# class CarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Car
#         fields='__all__'
        
#     def to_representation(self, instance):
#         data= super().to_representation(instance)
#         data['is_available']= instance.is_available
#         data['rent']=instance.rent
#         return data   

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        # fields = "__all__"
        fields =['name','short_name','code_registration','main_location','brand','model','price','capacity','owner','creator']


class CarSerializerReservation(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ["id", "name",  "code_registration", "image", "type"]

    def get_type(self, obj):
        return "Reservation"
    
    
class CarsSerializerRents(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ["id","name","code_registration","image","type"]

    def get_type(self, obj):
        return "Rent"
    
class CarsSerializerWithMainLocation(serializers.ModelSerializer):

    main_location = LocationsSerializer(many=False)

    class Meta:
        model = Car
        fields = [
            "id",
            "name",
            # "short_name",
            "code_registration",
            "location",
            "image",
            # "is_active",
            "to_the_location",
            "main_location",
        ]
        
        
class CarsReservationSerializer(serializers.ModelSerializer):
    start_year = serializers.SerializerMethodField(read_only=True)
    start_month = serializers.SerializerMethodField(read_only=True)
    start_day = serializers.SerializerMethodField(read_only=True)
    start_hour = serializers.SerializerMethodField(read_only=True)
    start_minute = serializers.SerializerMethodField(read_only=True)

    end_year = serializers.SerializerMethodField(read_only=True)
    end_month = serializers.SerializerMethodField(read_only=True)
    end_day = serializers.SerializerMethodField(read_only=True)
    end_hour = serializers.SerializerMethodField(read_only=True)
    end_minute = serializers.SerializerMethodField(read_only=True)

    type = serializers.SerializerMethodField(read_only=True)

    id_cars = CarSerializer(many=False) 
    location = LocationsSerializer(many=False)

    class Meta:
        model = Cars_Reservation
        fields = [
            "id",
            "id_cars",
            "client",
            "client_name",
            "client_document_type",
            "client_document_identification",
            "client_phone",
            "client_email",
            "date_from",
            "start_year",
            "start_month",
            "start_day",
            "start_hour",
            "start_minute",
            "date_to",
            "end_year",
            "end_month",
            "end_day",
            "end_hour",
            "end_minute",
            "note",
            "type",
            "location",
        ]

    def get_start_year(self, obj):
        start_year = obj.date_from.year
        return start_year

    def get_start_month(self, obj):
        start_month = obj.date_from.month
        return start_month

    def get_start_day(self, obj):
        start_day = obj.date_from.day
        return start_day

    def get_start_hour(self, obj):
        start_hour = obj.date_from.hour
        return start_hour

    def get_start_minute(self, obj):
        start_minute = obj.date_from.minute
        return start_minute

    def get_end_year(self, obj):
        end_year = obj.date_to.year
        return end_year

    def get_end_month(self, obj):
        end_month = obj.date_to.month
        return end_month

    def get_end_day(self, obj):
        end_day = obj.date_to.day
        return end_day

    def get_end_hour(self, obj):
        end_hour = obj.date_to.hour
        return end_hour

    def get_end_minute(self, obj):
        end_minute = obj.date_to.minute
        return end_minute

    def get_type(self, obj):
        if obj.date_from < timezone.now():
            return "Reservation delayed"
        else:
            return "Reservation"


# class CarsRentsSerializer(serializers.ModelSerializer):
#     start_year = serializers.SerializerMethodField(read_only=True)
#     start_month = serializers.SerializerMethodField(read_only=True)
#     start_day = serializers.SerializerMethodField(read_only=True)
#     start_hour = serializers.SerializerMethodField(read_only=True)
#     start_minute = serializers.SerializerMethodField(read_only=True)

#     end_year = serializers.SerializerMethodField(read_only=True)
#     end_month = serializers.SerializerMethodField(read_only=True)
#     end_day = serializers.SerializerMethodField(read_only=True)
#     end_hour = serializers.SerializerMethodField(read_only=True)
#     end_minute = serializers.SerializerMethodField(read_only=True)

#     type = serializers.SerializerMethodField(read_only=True)

#     id_cars = CarSerializer(many=False)
#     location = LocationsSerializer(many=False)

#     class Meta:
#         model = Cars_Rents
#         fields = [
#             "id",
#             "id_cars",
#             "client",
#             "client_name",
#             "client_document_type",
#             "client_document_identification",
#             "client_phone",
#             "client_email",
#             "deposit",
#             "deposit_currency",
#             "deposit_is_active",
#             "total_price",
#             "total_price_currency",
#             "total_price_is_paid",
#             "location",
#             "note",
#             "date_from",
#             "start_year",
#             "start_month",
#             "start_day",
#             "start_hour",
#             "start_minute",
#             "date_to",
#             "end_year",
#             "end_month",
#             "end_day",
#             "end_hour",
#             "end_minute",
#             "type",
#         ]

#     def get_start_year(self, obj):
#         start_year = obj.date_from.year
#         return start_year

#     def get_start_month(self, obj):
#         start_month = obj.date_from.month
#         return start_month

#     def get_start_day(self, obj):
#         start_day = obj.date_from.day
#         return start_day

#     def get_start_hour(self, obj):
#         start_hour = obj.date_from.hour
#         return start_hour

#     def get_start_minute(self, obj):
#         start_minute = obj.date_from.minute
#         return start_minute

#     def get_end_year(self, obj):
#         end_year = obj.date_to.year
#         return end_year

#     def get_end_month(self, obj):
#         end_month = obj.date_to.month
#         return end_month

#     def get_end_day(self, obj):
#         end_day = obj.date_to.day
#         return end_day

#     def get_end_hour(self, obj):
#         end_hour = obj.date_to.hour
#         return end_hour

#     def get_end_minute(self, obj):
#         end_minute = obj.date_to.minute
#         return end_minute

#     def get_type(self, obj):
#         if obj.date_to < timezone.now():
#             return "Delayed rental"
#         else:
#             return "Rental"


class CarsRentsSerializer(serializers.HyperlinkedModelSerializer):
    options = serializers.HyperlinkedRelatedField(
    view_name='CarRentViewSet',
    lookup_field = 'slug',
    many=True,
    read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name="cars:cars-rents")
    # client = serializers.PrimaryKeyRelatedField(
    #     read_only=True, 
    #     default=serializers.CurrentUserDefault())
    
    # Nested CarSerializer on read
    car = CarSerializer(read_only=True)
    
    # CarField on write
    # car_id = serializers.PrimaryKeyRelatedField(
    #     write_only=True,
    #     source='car',
    #     queryset=Car.objects.all(),
    #     label='Car')
           
    class Meta:
        model =Cars_Rents
        fields = ['url', 'id_cars', 'client', 'car','client_document_type','client_document_identification', 'date_from', 
                  'date_to', 'creator', 'client_phone','slug',
                  'total_price','options']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'total_price': {'read_only':True}
        }
                
    def validate(self, data):
        """
        Ensures that user can not book a car this is already booked
        in selected period
        """
        booking_start = data.get('date_from')
        booking_end = data.get('date_to')
        car = data.get('id_cars')
        instance = self.instance
        
        # Requested booking ends during existing booking, 
        # select sooner booking end date
        case_1 = Cars_Rents.objects.filter(car=car,
                                        booking_start__lte=booking_start,
                                        booking_end__gte=booking_start
        ).exists()
        # Requested booking starts during existing booking,
        # select later booking start date
        case_2 = Cars_Rents.objects.filter(car=car,
                                        booking_start__lte=booking_end,
                                        booking_end__gte=booking_end
        ).exists()
        # Requested booking starts and ends during existing booking
        case_3 = Cars_Rents.objects.filter(car=car,
                                        booking_start__gte=booking_start,
                                        booking_end__lte=booking_end
        ).exists()
        
        if not (instance and instance.car == car):
            if case_1:
                raise ValidationError(
                    """Requested booking ends during existing booking, \
                    select sooner booking end date"""
                    )
            elif case_2:
                raise ValidationError(
                    "Requested booking starts during existing booking, \
                        select later booking start date"
                    )
            elif case_3:
                raise ValidationError(
                    'Requested booking starts and ends during existing booking'
                    )
            return data
        return data
        
    def validate_booking_start(self, value):
        """
        Ensures that the earlies possible booking start day is today
        """
        booking_start = value
        today_value = timezone.now().today().date()
        if booking_start < today_value:
            raise ValidationError(
                f'Booking start date must be greater than {today_value}'
                )
        return super(CarsRentsSerializer, self).validate(value)
    
    def validate_booking_end(self, value):
        """
        Ensures that booking end date can not be before booking start date
        """
        data = self.get_initial()
        booking_start = data.get('booking_start')
        booking_start = datetime.strptime(booking_start, '%Y-%m-%d').date()
        booking_end = value
        if booking_end < booking_start:
            raise ValidationError(
                'Booking end date must be greater than booking start date'
                )
        return super(CarsRentsSerializer, self).validate(value)
            
    def save(self, **kwargs):
        """
        Include default for read_only `client` field
        """
        kwargs["client"] = self.fields["client"].get_default()
        return super().save(**kwargs)