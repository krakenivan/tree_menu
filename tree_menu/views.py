from django.shortcuts import render


def index(request):
    return render(request, "tree_menu/index.html")


def menu(request, menu):
    return render(request, "tree_menu/index.html")
