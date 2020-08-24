from django.urls import path
from . import views
from django.conf import settings
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.forms.utils import ErrorList


app_name = 'homepage'


class MyHackedPassView(auth_views.PasswordChangeView):
    success_url = reverse_lazy('homepage:password_change_done')


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
    path('password-change/', MyHackedPassView.as_view(),
         name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

