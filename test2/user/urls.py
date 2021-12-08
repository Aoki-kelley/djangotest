from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('jump/', views.jump, name='jump'),
    path('mine/', views.mine, name='mine'),
    path('reset_name/', views.reset_name, name='reset_name'),
    path('reset_ano/', views.reset_ano, name='reset_ano'),
    path('email_reg/', views.email_reg, name='email_reg'),
    path('email_reg/send_code/', views.send_code, name='send_code'),
    path('email_reg/email_prove/', views.email_prove, name='email_prove'),
    path('delete/<int:mid>/', views.delete, name='delete'),
]
