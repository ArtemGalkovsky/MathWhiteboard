from django.urls import path
from whiteboard.views import WhiteBoardView

app_name = 'whiteboard'
urlpatterns = [
    path("board/", WhiteBoardView.as_view(), name="board"),
]