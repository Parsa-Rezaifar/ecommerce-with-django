from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/',views.User_RegistrationView.as_view(),name='register'),
    path('login/',views.User_LoginView.as_view(),name='login'),
    path('logout/',views.User_LogoutView.as_view(),name='logout'),
    path('verify/',views.User_Registration_Verification_CodeView.as_view(),name='verification_code'),
]