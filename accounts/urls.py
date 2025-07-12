from django.urls import path, include
from .views.other_views import index

app_name = "accounts"
urlpatterns = [
    path("", index, name="index"), # Home page
    path("", include("accounts.urls_folder.friends_urls")),
    path("", include("accounts.urls_folder.registration_urls")),
]