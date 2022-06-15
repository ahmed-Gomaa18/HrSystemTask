from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('user/', views.get_user),
    path('login/', views.login, name='login'),
    path('register/', views.register),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),

    path('check-in/employee-<str:employee_pk>/', views.check_in, name="check_in"),
    path('check-out/employee-<str:employee_pk>/attendance-<str:attendance_pk>/', views.check_out, name="check_out"),
    path('list-attendances/employee-<str:employee_pk>/', views.list_attendances, name="list_attendances"),
    path('list-attendances-all/', views.list_attendances_all, name="list_attendances_all"),

    path('check-in-again/employee-<str:employee_pk>/attendance-<str:attendance_pk>/', views.check_in_again, name="check_in_again"),
    path('check-out-again/employee-<str:employee_pk>/attendance-<str:attendance_pk>/', views.check_out_again, name="check_out_again"),

]
