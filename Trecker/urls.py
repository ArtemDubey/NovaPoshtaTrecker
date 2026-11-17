from django.urls import path
from Trecker.views import home_view, parcel_list_view, parcel_detail_view, search_view

urlpatterns = [
    path('', home_view, name='home'),
    path('parcels/', parcel_list_view, name='parcel_list'),
    path('parcels/<str:track_number>/', parcel_detail_view, name='parcel_detail'),
    path('search/', search_view, name='search'),
]