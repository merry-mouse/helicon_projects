from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    PhotoListView,
    PhotoDetailView,
    PhotoCreateView,
    PhotoUpdateView,
    PhotoDeleteView,
    PhotoMyListView,
    UserPhotosDetailView
)
    
# namespace of the app
app_name = 'photo'    
urlpatterns = [
    path('', PhotoListView.as_view(), name='list'),

    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='detail'),

    path('photo/create/', PhotoCreateView.as_view(), name='create'),

    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),

    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),

    path('photo/mylist/', login_required(PhotoMyListView.as_view()), name='mylist'),

    path('photo/myphotodetail/<int:pk>/', UserPhotosDetailView.as_view(), name='userphotosdetail'),

]
