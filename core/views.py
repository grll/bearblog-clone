from django.shortcuts import render


def homepage(request):
    """Homepage view with marketing content."""
    return render(request, "homepage.html")
