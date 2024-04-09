from django.urls import path
from likes import views

urlpatterns = [
    path('likes/', views.LikeList.as_view(), name='likes'),
    path('likes/<int:pk>/', views.LikeDetail.as_view(), name='likes_detail'),
]
