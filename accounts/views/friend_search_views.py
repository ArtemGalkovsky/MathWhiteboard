from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import FriendSearchForm
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from ..models import FriendshipInvite, Friendship
from MathWhiteboard.config import ACCOUNTS_HANDLE_FRIENDSHIP_REQUEST_NO_PERMISSION

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base_with_header_menu.html")

@login_required
@require_http_methods(["GET"])
def search_friend(request: HttpRequest) -> HttpResponse:
    form = FriendSearchForm(request.GET)

    users = ()
    if form.is_valid():
        query = form.cleaned_data.get("query")

        if query:
            users = User.objects.filter(username__icontains=query) \
                .exclude(id=request.user.id)
    else:
        form = FriendSearchForm()

    context = {"form": form, "users": users}
    return render(request, "search_friend.html",
                  context)


@login_required
@require_http_methods(["POST"])
def send_friend_request(request: HttpRequest, receiver_id: int) -> HttpResponse:
    receiver = get_object_or_404(User, pk=receiver_id)

    if request.user.id == receiver.id:
        messages.error(request, "You can't send a friend request to yourself")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if Friendship.objects.filter(user1=request.user, user2=receiver).exists():
        messages.error(request, "You are already friends")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    friendship_invite = FriendshipInvite.objects.filter(sender=request.user, receiver=receiver)
    if not friendship_invite.exists():
        FriendshipInvite.objects.create(sender=request.user, receiver=receiver)
    else:
        messages.error(request, "Friendship invite already sent.")

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_http_methods(["GET"])
def friendship_requests(request: HttpRequest) -> HttpResponse:
    requests = FriendshipInvite.objects.filter(receiver=request.user) \
        .select_related("sender").only("sender__username", "created_at")

    return render(request, "friend_requests.html", {"requests": requests})

@login_required
@require_http_methods(["POST"])
def friendship_request_accept(request: HttpRequest, invite_id: int) -> HttpResponse:
    invite = get_object_or_404(FriendshipInvite.objects.select_related("sender", "receiver"), pk=invite_id)

    if invite.receiver != request.user:
        return HttpResponseForbidden(ACCOUNTS_HANDLE_FRIENDSHIP_REQUEST_NO_PERMISSION)

    invite.accept()

    return redirect("accounts:friendship_requests")

@login_required
@require_http_methods(["POST"])
def friendship_request_reject(request: HttpRequest, invite_id: int) -> HttpResponse:
    invite = get_object_or_404(FriendshipInvite, pk=invite_id)
    invite.reject()

    return redirect("accounts:friendship_requests")

