from django import views
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from accounts.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import FriendSearchForm, UserRegistrationForm, UserEnterRegistrationCodeForm
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from .models import FriendshipInvite, Friendship
from MathWhiteboard.config import ACCOUNTS_HANDLE_FRIENDSHIP_REQUEST_NO_PERMISSION
from .service.registration_utls import generate_new_code, get_hash_from_email, save_registration_code_to_cache, \
    compare_registration_codes


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base_with_header_menu.html")

@login_required
@require_http_methods(["GET"])
def search_friend(request: HttpRequest) -> HttpResponse:
    form = FriendSearchForm(request.GET)

    found = False
    users = ()
    if form.is_valid():
        query = form.cleaned_data.get("query")

        if query:
            users = User.objects.filter(username__icontains=query) \
                .exclude(id=request.user.id)
            if not users:
                found = True
    else:
        form = FriendSearchForm()

    context = {"form": form, "users": users, "found": found}
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

class UserRegistrationView(views.View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request,
                      "registration.html",
                      {
                          "form": UserRegistrationForm()
                      })

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            code = generate_new_code()
            hashed_email = get_hash_from_email(form.cleaned_data["email"])
            save_registration_code_to_cache(hashed_email, code)

            print(f"CODE FOR EMAIL {hashed_email} IS: {code}")

            request.session["email"] = hashed_email
            return redirect("accounts:enter_registration_code")

        return render(request,
                      "registration.html",
                      {
                          "form": form
                      })


class UserEnterRegistrationCodeView(views.View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "registration_code_enter.html", {
            "form": UserEnterRegistrationCodeForm()
        })

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserEnterRegistrationCodeForm(request.POST)

        if not form.is_valid():
            form.add_error("code", "Code cannot be empty")
        elif not request.session.get("email"):
            form.add_error("code", "Session expired :( Please try again")
        elif not compare_registration_codes(request.session["email"], form.cleaned_data["code"]):
            form.add_error("code", "Invalid code")
        else:
            redirect("accounts:registration_set_password")

        return render(request, "registration_code_enter.html", {
            "form": form
        })

class UserSetPasswordRegistrationView(views.View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(request, "OK")

def send_code(request: HttpRequest) -> HttpResponse:
    send_mail(
        'Subject here',
        'Here is the message body.',
        'no-reply@forgottensymbols.moscow',  # Overrides DEFAULT_FROM_EMAIL if provided
        ['steamliteops@proton.me'],
        fail_silently=False,  # Set to True to suppress exceptions on failure
    )

    return redirect("accounts:index")