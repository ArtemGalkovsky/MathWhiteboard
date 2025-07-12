from django.urls import path
from ..views.registration_views import (send_code, UserRegistrationView, UserEnterRegistrationCodeView,
                                       UserSetPasswordRegistrationView)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("send_code/", send_code, name="send_code"),
    path("enter_registration_code/", UserEnterRegistrationCodeView.as_view(), name="enter_registration_code"),
    path("registration_set_password/", UserSetPasswordRegistrationView.as_view(), name="registration_set_password")
]