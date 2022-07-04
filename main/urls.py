from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('addEmp/', views.addEmp),
    path('updateEmp/<empid>', views.updateEmp),
    path('showEmp/', views.showEmp),
    path('delEmp/', views.delEmp),
    path('delEmpID/<empid>', views.delEmpID),
]