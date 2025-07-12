from django.urls import path
from ..views.friend_search_views import (search_friend, friendship_request_reject, friendship_request_accept,
                                        friendship_requests, send_friend_request)

urlpatterns = [
    path("find_my_friend/", search_friend, name="friend_search"),
    path("send_friend_request/<int:receiver_id>", send_friend_request, name="send_friend_request"),
    path("friendship_requests/", friendship_requests, name="friendship_requests"),
    path("friendship_accept/<int:invite_id>/", friendship_request_accept, name="friendship_accept"),
    path("friendship_reject/<int:invite_id>/", friendship_request_reject, name="friendship_reject"),
]
