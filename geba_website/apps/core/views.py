# Create your views here.
from django.shortcuts import render

# Create your views here.
# render(request, rendered_html, optional_dictionary)


def index(request):
    """the core page for GEBA Website"""
    return render(request, 'core/home.html')
