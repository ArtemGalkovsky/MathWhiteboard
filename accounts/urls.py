from django.urls import path
from .views import index, search_friend, send_friend_request, friendship_requests, friendship_request_accept, \
    friendship_request_reject, registration, send_code

app_name = "accounts"

urlpatterns = [
    path("", index, name="index"), # Home page
    path("find_my_friend/", search_friend, name="friend_search"),
    path("send_friend_request/<int:receiver_id>", send_friend_request, name="send_friend_request"),
    path("friendship_requests/", friendship_requests, name="friendship_requests"),
    path("friendship_accept/<int:invite_id>/", friendship_request_accept, name="friendship_accept"),
    path("friendship_reject/<int:invite_id>/", friendship_request_reject, name="friendship_reject"),
    path("register/", registration, name="register"),
    path("send_code/", send_code, name="send_code")
]