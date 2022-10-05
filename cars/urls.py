from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # CARS
    
    path('api/car/',views.CarList.as_view()),
    path('api/car/new',views.CarCreate.as_view()),
    path('api/car/<int:id>/',views.CarRetrieveUpdateDestroy.as_view()),
    path('api/car/search',views.searchCarView.as_view()),
    
    
    
    # path("api/car/image/upload/", views.carUploadImage, name="car-upload-image"),
    # path("api/new/cars/upload/", views.newCarUploadImage, name="new-car-upload-image"),
    # path("api/car/", views.getCars, name="cars-list"),
    # path("api/car/create/", views.createCar, name="create-car"),
    # path("api/car/<str:pk>/", views.getCarById, name="get-car-by-id"),
    # path("api/car/update/<str:pk>/", views.updateCar, name="car-update"),
    
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
    
    # carRent
    
    # path("rent/car/create/", views.createRentCar, name="create-rent-car"),
    # path("rents/list/car/<str:pk>/", views.listRentsCar, name="list-rents-car"),
    # path("rent/edit/<str:pk>/", views.editCarRent, name="edit-rent"),
    
    # car pick-up
    
    
    # path(
    #     "<str:pk>/rent-details/",
    #     views.getRentDetailsByCarId,
    #     name="get-rent-details-by-car-id",
    # ),
    # path("rent/update/<str:pk>/", views.carUpdateRent, name="car-update-rent"),
    
    
    
    
]
router = DefaultRouter()
router.register(r'rent', views.cars_rentsViewSet, basename='CarRentViewSet')
urlpatterns = router.urls
