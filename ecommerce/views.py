from django.shortcuts import render


def home_page(request):
    context = {
        "title": "WoW!",
        "content": "Welcome to the Best Shopping at Web",
        "premium_content": "Your now login try for logout an other times :/"
    }
    return render(request, "home_page.html", context)
