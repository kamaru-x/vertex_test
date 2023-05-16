from django.urls import path
from u_auth import views

urlpatterns = [
    path('',views.signin,name='sign-in'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('sign-out/',views.signout,name='sign-out'),
    path('salesboard/',views.salesboard,name='salesboard'),
    path('change-password',views.changepassword,name='change-password'),
    path('change-salesman-password/<int:id>/',views.change_salesman_password,name='change-salesman-password')
]