from django.urls import path

from . import views

urlpatterns = [
    path('put/', views.leave_massage, name='massage'),
    path('reply/<mid>/', views.leave_reply, name='reply'),
    path('detail/<mid>/', views.detail, name='detail'),
    path('random/', views.message_random, name='random'),
]
