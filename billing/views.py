import stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.http import is_safe_url


stripe.api_key = "sk_test_xsB0ceSWejUXhmSJSlOnqitJ00TTZHqDU"

STRIPE_PUB_KEY = 'pk_test_xM90FAQHNuiRyxScNdeT1POR00a0jpuSPZ'


def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("Error", status_code=401)

