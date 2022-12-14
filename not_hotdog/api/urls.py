from django.urls import path
from . import views
 

urlpatterns = [

    path('photos/', views.PhotoList.as_view()),

    path('get_detail/<int:pk>/', views.PhotoDetailGetView.as_view()),

    path('update_detail/<int:pk>/', views.PhotoDetailPutDeleteView.as_view()),
]