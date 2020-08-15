from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
app_name = 'homepage'

urlpatterns = [
    path('find_master/', views.find_master, name='find_master'),
    path('<int:id_>/<str:district>/',
         views.people_details,
         name='people_details'),
    path('', views.start_page, name='start_page'),
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

