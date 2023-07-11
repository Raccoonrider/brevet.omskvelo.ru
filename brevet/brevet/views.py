import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

# --- Static pages ---
def faq(request):
    return render(request, "faq.html")

def calc(request):
    return render(request, "calc.html")

def csrf_failure(request, *args, **kwargs):
    return redirect(request.META.get('HTTP_REFERER'))

def loaderio(request, token):
    if token == os.environ["LOADERIO_TOKEN"]:
        return HttpResponse(f"loaderio-{token}")
    else:
        raise Http404