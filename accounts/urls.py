from django.urls import path


from .views import (
    contact_page,
    LoginView,
    logout_view,
    RegisterView,
    guest_register_view)


app_name = 'accounts'

urlpatterns = [
    path(r'contact/', contact_page, name='contact'),
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'register/guest/', guest_register_view, name='guest'),
    path(r'logout/', logout_view, name='logout'),
    path(r'register/', RegisterView.as_view(), name='register'),
]