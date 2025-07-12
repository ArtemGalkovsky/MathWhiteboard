from django import views
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from accounts.forms import UserRegistrationForm, UserEnterRegistrationCodeForm
from django.http import HttpRequest, HttpResponse
from ..service.registration_utls import generate_new_code, get_hash_from_email, save_registration_code_to_cache, \
    compare_registration_codes


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

send_mail('РИО Я ТЕБЯ ЛЮБЛЮ', 'РИО ДАВАЙ ОБНИМАЦА ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️', 'no-reply@forgottensymbols.moscow', ['kovzunovichartemij@gmail.com'], fail_silently=False)
