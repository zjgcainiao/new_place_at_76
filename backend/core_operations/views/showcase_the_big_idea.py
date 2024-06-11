from .base import requests, render


def showcase_the_big_idea(request):
    return render(request, 'core_operations/60_the_big_idea.html')