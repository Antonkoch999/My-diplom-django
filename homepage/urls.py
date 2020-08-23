from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
app_name = 'homepage'

urlpatterns = [
    path('find_master/', views.find_master, name='find_master'),
    path('<int:id_>/',
         views.people_details,
         name='people_details'),
    path('', views.start_page, name='start_page'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.view_profile, name='profile'),
    path('edit/', views.edit_profile, name='edit'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

