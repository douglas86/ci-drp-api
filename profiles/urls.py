from django.urls import path, include
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view({'get': 'retrieve'}), name='profile-list'),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view({'get': 'retrieve'}), name='profile_detail'),
]
