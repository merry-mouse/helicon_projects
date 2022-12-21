from django.urls import path
from . import views
 

urlpatterns = [

    path('photos/', views.PhotoList.as_view()), # to see all listed photos

    path('get_detail/<int:pk>/', views.PhotoDetailGetView.as_view()), # to see the detail of one photo

    path('update_detail/<int:pk>/', views.PhotoDetailPutDeleteView.as_view()), # to change the detail
]