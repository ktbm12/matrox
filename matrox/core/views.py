from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def service(request):
    return render(request, "service.html")


def liste(request):
    return render(request, "liste.html")


def detail(request):
    return render(request, "detail.html")