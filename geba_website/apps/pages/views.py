from django.views.generic import DetailView
from .models import Page
from django.shortcuts import get_object_or_404
# Create your views here.


class PageDetailView(DetailView):
    """This view will be used to GET the detail data"""
    # success_msg = 'Comment Added!'
    model = Page  # generic views need to know which model to act upon
    template_name = 'pages/detail.html'  # tells the view to use this template instead of it's default


class HomeView(DetailView):
    """This view will be used to GET the detail data"""
    # success_msg = 'Comment Added!'
    model = Page  # generic views need to know which model to act upon
    template_name = 'pages/detail.html'  # tells the view to use this template instead of it's default

    def get_object(self):
        # make it so only the admin can see items in the future or that are drafts
        # don't use annotate, use vote_by in this case, annotate only works when __iter__ is called
        instance = get_object_or_404(Page, slug='home')
        return instance