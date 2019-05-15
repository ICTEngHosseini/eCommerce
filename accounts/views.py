from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from .forms import ContactForm, LoginForm, RegisterForm, GuestForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.utils.http import is_safe_url
from .models import GuestEmail
from django.http import JsonResponse, HttpResponse
from django.views.generic import CreateView, FormView
from .signals import user_logged_in


@csrf_protect
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact",
        "content": "Contact View",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Thank you Sexy ;)"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, "contact/view.html", context)


@csrf_protect
def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/accounts/register/")
    return render(request, "accounts/guest_email.html", context)


def logout_view(request):
    logout(request)
    return redirect('home')


#####//////////\\\\\\\\\\####
#        Class base         #
#           Views           #
#####\\\\\\\\\\//////////####


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = '/login/'

#####//////////\\\\\\\\\\####
#       Function base       #
#           Views           #
#####\\\\\\\\\\//////////####

# User = get_user_model()

# @csrf_protect
# def login_page(request):
#     login_form = LoginForm(request.POST or None)
#     context = {
#         "login_form": login_form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if login_form.is_valid():
#         username = login_form.cleaned_data.get("username")
#         password = login_form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             # Return an 'invalid login' error message.
#             print("invalid input")
#     return render(request, "accounts/login.html", context)


# @csrf_protect
# def register_page(request):
#     register_form = RegisterForm(request.POST or None)
#     context = {
#         "register_form": register_form
#     }
#     if register_form.is_valid():
#         register_form.save()
#         # print(register_form.cleaned_data)
#         # username = register_form.cleaned_data.get("username")
#         # email = register_form.cleaned_data.get("email")
#         # password = register_form.cleaned_data.get("password")
#         # User.objects.create_user(username, email, password)
#     return render(request, "accounts/register.html", context)