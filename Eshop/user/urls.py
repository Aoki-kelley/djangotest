from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register&<role>/', views.register, name='register'),
    path('email_prove/<username>/', views.email_prove, name='email_prove'),
    path('email_prove/', views.raise_wrong),
    path('send_again/<username>&<label>/', views.send_again, name='send_again'),
    path('send_again/', views.raise_wrong),
    path('mine/', views.mine, name='mine'),
    path('reset_name/', views.reset_name, name='reset_name'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_image/', views.reset_image, name='reset_image'),
    path('add_money/', views.add_money, name='add_money'),
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),
]
