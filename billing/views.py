import stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render


stripe.api_key = "sk_test_xsB0ceSWejUXhmSJSlOnqitJ00TTZHqDU"

STRIPE_PUB_KEY = 'pk_test_xM90FAQHNuiRyxScNdeT1POR00a0jpuSPZ'


def payment_method_view(request):
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY})


def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message": "Done"})
    return HttpResponse("Error", status_code=401)

