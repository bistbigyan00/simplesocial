from django.contrib.auth import views as auth_views
from accounts import views
from django.urls import path

#for template tagging
app_name = 'accounts'

#login and logout has automatic views
urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.SignUP.as_view(),name='signup'),
]
