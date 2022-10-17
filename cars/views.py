from urllib import response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .serializer import CarSerializer
from .models import Car 
from django.utils import timezone
from rest_framework import viewsets
from django.core.cache import cache
from rest_framework import filters
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
import pytz 

# Create your views here. 
# # Create your views here.



class CarList(generics.ListCreateAPIView):
    queryset=Car.objects.all()
    serializer_class=CarSerializer
    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale',None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Car.objects.all()
        if on_sale.lower()=='true':
            now=timezone.now()
            return queryset.filter(
                sale_start_lte=now,
                sale_end_gte=now,
            )
            
        return queryset
    
    
    
class CarCreate(CreateAPIView):
    serializer_class = CarSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            rent = request.data.get('price')
            if rent is not None and float(rent) <= 0.0:
                raise ValidationError({'rent':'Must be above 0'})
        except ValueError:
            raise ValidationError({'rent':'a validate number is required'})  
        return super().create(request, *args, **kwargs)


class CarRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    lookup_field ='id'
    serializer_class= CarSerializer
    
    def delete(self,request,*args, **kwargs):
        car_id = request.data.get('id')
        response = super().delete(request,*args, **kwargs)
        if response.status_code == 204:
            cache.delete('car_data_{}'.format(car_id))
        return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request,*args, **kwargs)
        if response.status_code== 200:  
            car = response.data
            # cache.set('car_data_{}'.format(car['id'])),{
            cache.set('car_data_',id),{
                'name': car['name'],
                'description': car['description'],
                'image':car['image'],
                'rent': car['rent'],
            }
        return response
    
class searchCarView(generics.ListAPIView):
        queryset = Car.objects.all()
        serializer_class = CarSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['name', 'description']



# new views 


# LOCATIONS
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getLocations(request):
    locations = Location.objects.filter(is_active=True).order_by("short_name")
    serializer = LocationsSerializer(locations, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def createLocation(request):
    data = request.data
    creator_str = str(data["creator"])
    try:
        location = Location.objects.create(
            name=data["name"],
            short_name=data["shortName"],
            # creator=creator_str,
            # supp_unique_var=data["supp_unique_var"],
        )

        serializer = LocationsSerializer(location, many=False)
        return Response(serializer.data)
    except:
        message = {"detail": "The given name already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getLocationById(request, pk):
    user = Location.objects.get(id=pk)
    serializer = LocationsSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateLocation(request, pk):
    location = Location.objects.get(id=pk)

    data = request.data
    location.name = data["name"]
    location.short_name = data["shortName"]
    # location.is_active = data["isActive"]

    location.save()
    serializer = LocationsSerializer(location, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def uploadImage(request):
    data = request.data
    location_id = data["location_id"]
    location = Location.objects.get(id=location_id)
    # location.image = request.FILES.get("image")
    location.save()
    serializer = LocationsSerializer(location, many=False)
    return Response(serializer.data)


# @api_view(["POST"])
# def newLocationUploadImage(request):
#     data = request.data
#     supp_unique = data["suppUniqueVar"]

#     locationWithImage = Location.objects.get(supp_unique_var=supp_unique)
#     locationWithImage.image = request.FILES.get("image")
#     locationWithImage.save()

#     serializer = LocationsSerializer(locationWithImage, many=False)
#     return Response(serializer.data)


# CARS

# @api_view(["GET"])
# @permission_classes([IsAdminUser])
# def getCars(request):
#     cars = Car.objects.all().order_by("short_name")
#     serializer = CarSerializer(cars, many=True)
#     return Response(serializer.data)


# @api_view(["POST"])
# # @permission_classes([IsAdminUser])
# def createCar(request):
#     data = request.data
#     user = request.user
#     obj_location = Location.objects.get(id=data["location"])

#     try:
#         print(222222)
#         car = Car.objects.create(
#             name=data["name"],
#             short_name=data["shortName"],
#             code_registration=data["codeRegistration"],
#             main_location=obj_location,
#             owner= user,
#             creator=data["creator"],
#             # Flocation=data["Flocation"],  
#             # to_the_location=data["Tlocation"],
#         )
#         print('11111')      
#         serializer = CarSerializer(car, many=False)
#         return Response(serializer.data)

#     except:
#         message = {"detail": "The registration code provided already exists"}
#         return Response(message, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def carUploadImage(request):
#     data = request.data
#     car_id = data["car_id"]
#     car = Car.objects.get(id=car_id)

#     car.image = request.FILES.get("image")
#     car.save()

#     serializer = CarSerializer(car, many=False)
#     return Response(serializer.data)


# @api_view(["POST"])
# def newCarUploadImage(request):
#     data = request.data
#     print(data)
#     codeRegistration = data["code_registration"]
#     car = Car.objects.get(code_registration=codeRegistration)
#     car.image = request.FILES.get("image")
#     car.save()
#     serializer =CarSerializer(car, many=False)
#     return Response(serializer.data)


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def getCarById(request, pk):
#     car = Car.objects.get(id=pk)
#     serializer = CarsSerializerWithMainLocation(car, many=False)
#     return Response(serializer.data)


# @api_view(["PUT"])
# @permission_classes([IsAuthenticated])
# def updateCar(request, pk):
    data = request.data
    obj_location = Location.objects.get(id=data["main_location"])
    car = Car.objects.get(id=pk)
    car_ARC = Cars_ARC.objects.create(
        id_car=car.id,
        id_location=car.main_location.id,
        name=car.name,
        short_name=car.short_name,
        code_registration=car.code_registration,
        creator_ARC=data["creator"],
        # type=data["type"],
        on_the_way=car.on_the_way,
        location=car.location,
        to_the_location=car.to_the_location,
        come_back=car.come_back,
    )

    try:
        car.name = data["name"]
        car.short_name = data["shortName"]
        car.main_location = obj_location
        car.code_registration = data["codeRegistration"]
        car.is_active = data["isActive"]

        car.save()

        serializer = CarSerializer(car, many=False)

        return Response(serializer.data)

    except:
        message = {"detail": "The registration code provided already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # CARLIST BY LOCATION 
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCarListByLocationToRent(request, pk):
    carList = Car.objects.filter(
        location=pk, on_the_way=False
    ).order_by("short_name")
    serializer = CarSerializer(carList, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCarListByLocationInUse(request, pk):
    carRent = Cars_Rents.objects.filter(location=pk, is_active=True).order_by("date_to")

    carSerializerRents = CarsRentsSerializer(carRent, many=True)

    return Response(carSerializerRents.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCarListByLocationToDo(request, pk):

    today_plus = timezone.now() + timedelta(hours=12)
    today_minus = timezone.now() - timedelta(hours=12)

    carResArchive = Cars_Reservation.objects.filter(
        date_from__lt=today_minus, is_active=True
    )

    for i in carResArchive:
        i.is_active = False
        i.type_change = "delete automatically"
        i.date_of_change = timezone.now()
        i.save()

    carRes = Cars_Reservation.objects.filter(
        location=pk, date_from__lt=today_plus, date_from__gt=today_minus, is_active=True
    ).order_by("date_from")

    carRent = Cars_Rents.objects.filter(
        location=pk, date_to__lt=today_plus, is_active=True
    ).order_by("date_to")

    carSerializerReservation = CarsReservationSerializer(carRes, many=True)
    carSerializerRents = CarsRentsSerializer(carRent, many=True)

    combine_serializers = carSerializerRents.data + carSerializerReservation.data

    return Response(combine_serializers)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCarListFilterReservation(request, pk):
    today = timezone.now() + timedelta(hours=12)
    today_minus = timezone.now() - timedelta(hours=12)
    today_plus = timezone.now() + timedelta(hours=12)
    carRes = Cars_Reservation.objects.filter(
        location=pk, date_from__lt=today_plus, date_from__gt=today_minus, is_active=True
    ).order_by("date_from")

    serializer = CarsReservationSerializer(carRes, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCarListFilterRents(request, pk):
    today = timezone.now() + timedelta(hours=12)
    carRent = Cars_Rents.objects.filter(
        location=pk, date_to__lt=today, is_active=True
    ).order_by("date_to")

    serializer = CarsRentsSerializer(carRent, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCarListByLocationReservations(request, pk):
    today = timezone.now()
    carList = Car.objects.filter(
        carReservations__location=pk,
        carReservations__date_from__gt=today,
        carReservations__is_active=True,
    ).order_by("short_name")

    unique_cars_list = []
    for car in carList:
        if car not in unique_cars_list:
            unique_cars_list.append(car)

    serializer = CarSerializer(unique_cars_list, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCarListByLocationNewReservations(request, pk):

    carList = Car.objects.filter(location=pk).order_by("short_name")

    serializer = CarSerializer(carList, many=True)

    return Response(serializer.data)


# CAR RESERVATION 

def time_converter(time):
    s = time
    hours, minutes, seconds = (["0", "0"] + s.split(":"))[-3:]
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds)
    miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
    return miliseconds

def convertDate(str):
    date = str

    year = ""
    mounth = ""
    day = ""
    hour = ""
    minutes = ""
    a = 0
    b = 0
    for i in date:
        if i == "-" and b == 0:
            year = date[0:a]
            if date[a + 2] == "-":
                mounth = date[5 : a + 2]
            else:
                mounth = date[5 : a + 3]
            b = 1
        if i == "-" and b == 1:
            if date[a + 2] == " ":
                day = date[a + 1 : a + 2]
            else:
                day = date[a + 1 : a + 3]
        if i == " ":
            if date[a + 2] == ":":
                hour = date[a + 1 : a + 2]
            else:
                hour = date[a + 1 : a + 3]
        if i == ":":
            minutes = date[a + 1 :]
        a += 1
    return datetime(
        int(year), int(mounth), int(day), int(hour), int(minutes), tzinfo=pytz.UTC
        # int(2022), int(9), int(2), int(4), int(12), tzinfo=pytz.UTC
        # int(year), int(mounth),int(day),  tzinfo=pytz.UTC
    )

    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createReservationCar(request):
    data = request.data
    date_obj_start = convertDate(data["dateFrom"])
    date_obj_end = convertDate(data["dateTo"])

    obj_car = Car.objects.get(id=data["idCars"])
    obj_location = Location.objects.get(id=data["location"])

    obj_reservations = Cars_Reservation.objects.filter(
        id_cars=data["idCars"], is_active=True
    )
    obj_rents = Cars_Rents.objects.filter(id_cars=data["idCars"], is_active=True)

    if data["location"] == obj_car.Flocation:
        extension = timedelta(milliseconds=int(data["timeReservation"]))
    else:
        extension = timedelta(
            milliseconds=int(data["timeReservation"]) + int(data["transferTime"])
        ) 

    for res in obj_reservations:
        if date_obj_start > (res.date_from - extension) and date_obj_start < (
            res.date_to + extension
        ):
            return Response("date range exists for dataStart")
        if date_obj_end > (res.date_from - extension) and date_obj_end < (
            res.date_to + extension
        ):
            return Response("date range exists for dataEnd")
        if date_obj_start < (res.date_from - extension) and date_obj_end > (
            res.date_to + extension
        ):
            return Response("included date range")

    for ren in obj_rents:
        if date_obj_start > (ren.date_from - extension) and date_obj_start < (
            ren.date_to + extension
        ):
            return Response("lease date range exists for dataStart")
        if date_obj_end > (ren.date_from - extension) and date_obj_end < (
            ren.date_to + extension
        ):
            return Response("lease date range exists for dataEnd")
        if date_obj_start < (ren.date_from - extension) and date_obj_end > (
            ren.date_to + extension
        ):
            return Response("included date range for the lease")

    try:
        car_reservation = Cars_Reservation.objects.create(
            id_cars=obj_car,
            client_name=data["name"],
            client_document_type=data["documentType"],
            client_document_identification=data["IdNumber"],
            client_phone=data["phone"],
            client_email=data["email"],
            date_from=date_obj_start,
            date_to=date_obj_end,
            note=data["note"],
            location=obj_location,
            creator=data["creator"],
        )

        return Response("Success",status=status.HTTP_201_CREATED)

    except:
        message = {"detail": "Something went wrong"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listReservationCar(request, pk, loc):
    print(pk,loc)

    if loc == "0":
        carListReservation = Cars_Reservation.objects.filter(id_cars=pk, is_active=True)
    else:
        carListReservation = Cars_Reservation.objects.filter(
            id_cars=pk,location=loc
        )

    carListReservationGroupBy = carListReservation.order_by("date_from")
    serializer = CarsReservationSerializer(carListReservationGroupBy, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def deleteReservation(request, pk):
    data = request.data
    reservationForDeletion = Cars_Reservation.objects.get(id=pk)

    reservationForDeletion.is_active = False
    reservationForDeletion.date_of_change = timezone.now()
    reservationForDeletion.creator_change = data["creator"]
    # reservationForDeletion.type_change = data["type_change"]
    reservationForDeletion.id_arc = data["id"]

    reservationForDeletion.save()
    return Response("Reservation was deleted")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getReservationById(request, pk):
    reservation = Cars_Reservation.objects.get(id=pk)

    serializer = CarsReservationSerializer(reservation, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateReservation(request, pk):

    data = request.data
    reservation = Cars_Reservation.objects.get(id=pk)

    obj_car = Car.objects.get(id=reservation.id_cars.id)
    date_obj_start = convertDate(data["dateFrom"])
    date_obj_end = convertDate(data["dateTo"])

    obj_reservations = Cars_Reservation.objects.filter(
        id_cars=reservation.id_cars, is_active=True
    ).exclude(id=pk)

    obj_rents = Cars_Rents.objects.filter(id_cars=reservation.id_cars, is_active=True)
    obj_location = Location.objects.get(id=data["location"])

    for res in obj_reservations:
        if data["location"] == res.location:
            extension = timedelta(milliseconds=data["timeReservation"])
        else:
            extension = timedelta(
                milliseconds=data["timeReservation"] + data["transferTime"]
            )

        if date_obj_start > (res.date_from - extension) and date_obj_start < (
            res.date_to + extension
        ):
            return Response("date range exists for dataStart")
        if date_obj_end > (res.date_from - extension) and date_obj_end < (
            res.date_to + extension
        ):
            return Response("date range exists for dataEnd")
        if date_obj_start < (res.date_from - extension) and date_obj_end > (
            res.date_to + extension
        ):
            return Response("included date range")

    for ren in obj_rents:
        if data["location"] == ren.location:
            extension = timedelta(milliseconds=data["timeReservation"])
        else:
            extension = timedelta(
                milliseconds=data["timeReservation"] + data["transferTime"]
            )

        if date_obj_start > (ren.date_from - extension) and date_obj_start < (
            ren.date_to + extension
        ):
            return Response(" lease date range exists for dataStart")
        if date_obj_end > (ren.date_from - extension) and date_obj_end < (
            ren.date_to + extension
        ):
            return Response("lease date range exists for dataEnd")
        if date_obj_start < (ren.date_from - extension) and date_obj_end > (
            ren.date_to + extension
        ):
            return Response("included date range for the lease")

    try:
        reservation.is_active = False
        reservation.date_of_change = timezone.now()
        reservation.creator_change = data["creator"]
        # reservation.type_change = data["type"]
        reservation.id_arc = data["id"]
        reservation.save()
    except:
        message = {"detail": "Something went wrong with the Udated data"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    try:
        car_reservation = Cars_Reservation.objects.create(
            id_cars=obj_car,
            client_name=data["name"],
            client_document_type=data["documentType"],
            client_document_identification=data["IdNumber"],
            client_phone=data["phone"],
            client_email=data["email"],
            date_from=date_obj_start,
            date_to=date_obj_end,
            note=data["note"],
            location=obj_location,
            creator=data["creator"],
            id_arc=data["id"],
            # type_change="create by update",
        )
    except:
        reservation.is_active = True
        reservation.save()
        message = {"detail": "Something went wrong while Update data"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    return Response("successful")


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def filterReservations(request):
    print(111111,request.user)
    data = request.data
    start_date = convertDate(data["date_from"])
    end_date = convertDate(data["date_to"])

    extension = timedelta(milliseconds=data["transfer_time"])

    cars_with_available_terms_list = []
    cars_not_available_list = []
    cars_rent_list = []
    unique_list = []
    unique_list2 = []
    car_without_reservations = []
    final_list = []

    obj_cars = Car.objects.filter(is_available=True)
    obj_res = Cars_Reservation.objects.filter(is_active=True)
    obj_rents = Cars_Rents.objects.filter(is_active=True)

    for car in obj_cars:
        for res in obj_res:
            if car.id == res.id_cars.id:
                if (
                    (res.date_from - extension) > start_date
                    and (res.date_from - extension) > end_date
                ) or (
                    (res.date_to + extension) < start_date
                    and (res.date_to + extension) < end_date
                ):
                    cars_with_available_terms_list.append(car)
                else:
                    cars_not_available_list.append(car)

    for car in obj_cars:
        for rent in obj_rents:
            if car.id == rent.id_cars.id:
                if (rent.date_to + extension) > start_date:
                    cars_rent_list.append(car)

    for i in cars_with_available_terms_list:
        if i not in unique_list:
            unique_list.append(i)

    for i in cars_not_available_list:
        if i not in unique_list2:
            unique_list2.append(i)

    combine_unique_lists = unique_list + unique_list2

    for i in obj_cars:
        if i not in combine_unique_lists:
            car_without_reservations.append(i)

    unique_available_cars_list = unique_list + car_without_reservations

    for i in unique_available_cars_list:
        if i not in cars_rent_list:
            final_list.append(i)

    serializer = CarSerializer(final_list, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getReservationList(request):
    carReservationList = Cars_Reservation.objects.filter(is_active=True).order_by(
        "date_from"
    )

    carSerializerReservations = CarsReservationSerializer(carReservationList, many=True)

    return Response(carSerializerReservations.data)



class cars_rentsViewSet(viewsets.ModelViewSet):
   
    serializer_class = CarsRentsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_cars', 'date_from', 'date_to']
    ordering_fields = ['date_from', 'date_to']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Cars_Rents.objects.all()
        else:
            return Cars_Rents.objects.filter(user=user)