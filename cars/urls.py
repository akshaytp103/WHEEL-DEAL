from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # CARS
    
    path('api/car/',views.CarList.as_view()),
    path('api/car/new',views.CarCreate.as_view()),
    path('api/car/<int:id>/',views.CarRetrieveUpdateDestroy.as_view()),
    path('api/car/search',views.searchCarView.as_view()),
    
    
    
    
    # carlistsbylocation 
    
    path(
        "mainpage/<str:pk>/car-list/to-rent/",
        views.getCarListByLocationToRent,
        name="get-carlist-by-location-to-rent",
    ),
    path(
        "mainpage/<str:pk>/car-list/in-use/",
        views.getCarListByLocationInUse,
        name="get-carlist-by-location-in-use",
    ),
    path(
        "mainpage/<str:pk>/car-list/to-do/",
        views.getCarListByLocationToDo,
        name="get-carlist-by-location-to-do",
    ),
    path(
        "mainpage/<str:pk>/car-list/reservations/",
        views.getCarListByLocationReservations,
        name="get-carlist-by-location-reservations",
    ),
    path(
        "mainpage/<str:pk>/car-list/new-reservation/",
        views.getCarListByLocationNewReservations,
        name="get-carlist-by-location-new-reservation",
    ),
    # carListByLocation - filters
    path(
        "mainpage/<str:pk>/car-list/fiter-reservations/",
        views.getCarListFilterReservation,
        name="get-carlist-by-location-fiter-reservations",
    ),
    path(
        "mainpage/<str:pk>/car-list/fiter-rents/",
        views.getCarListFilterRents,
        name="get-carlist-by-location-fiter-rents",
    ),
    path(
        "mainpage/<str:pk>/car-list/fiter-all/",
        views.getCarListByLocationToDo,
        name="get-carlist-by-location-fiter-all",
    ),
   
    # carReservation
    
    path(
        "api/filter/reservation/",
        views.filterReservations, 
        name="filter-reservations"
    ),
    path(
        "api/reservation/car/create/",
        views.createReservationCar,
        name="create-reservation-car",
    ),
    path(
        "api/reservation/list/car/<str:pk>/<str:loc>/",
        views.listReservationCar,
        name="list-reservation-car",
    ),
    path(
        "api/reservation/delete/<str:pk>/",
        views.deleteReservation,
        name="reservation-delete",
    ),
    path(
        "api/car/single/reservation/<str:pk>/edit/",
        views.getReservationById,
        name="get-reservation-by-id",
    ),
    path(
        "api/reservation/update/<str:pk>/",
        views.updateReservation,
        name="update-reservation",
    ),
    
]
router = DefaultRouter()

