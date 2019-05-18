from django.urls import path


from .views import payment_method_view, payment_method_create_view


app_name = 'billing'

urlpatterns = [
    path(r'payment-method/', payment_method_view, name='payment_method'),
    path(r'payment-method/create/', payment_method_create_view, name='payment_method_create'),
]