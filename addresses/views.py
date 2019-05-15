from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_protect
from .forms import AddressForm
from .models import Address
from billing.models import BillingProfile


@csrf_protect
def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or None
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'address')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()

            request.session[address_type + "_address_id"] = instance.id
            shipping_address_id = request.session.get("shipping_address_id", None)
            billing_address_id = request.session.get("billing_address_id", None)
        else:
            print("Goddammit Error is happen")
            return redirect("carts:checkout")

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return render(request, "addresses/form.html", context)


@csrf_protect
def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or None

        if request.method == "POST":
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'address')
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect("carts:checkout")