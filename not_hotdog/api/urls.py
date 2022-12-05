from django.urls import path
from . import views
 

urlpatterns = [

    path('photos/', views.PhotoList.as_view()),

    path('photo_detail/<int:pk>/', views.PhotoDetail.as_view()),
]