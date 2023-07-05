import os

from django.shortcuts import render
from django.http import HttpResponse, Http404

# --- Static pages ---
def faq(request):
    return render(request, "faq.html")

def calc(request):
    return render(request, "calc.html")

def loaderio(request, token):
    if token == os.environ["LOADERIO_TOKEN"]:
        return HttpResponse(f"loaderio-{token}")
    else:
        raise Http404