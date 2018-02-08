from django.shortcuts import render
from django.views.generic import DetailView
from .models import AboutMe
# Create your views here.


def index(request):
    return render(request, 'about_me/detail.html')


class AboutMeDetailView(DetailView):
    model = AboutMe  # generic views need to know which model to act upon
    template_name = 'about_me/detail.html'  # tells the view to use this template instead of it's default
