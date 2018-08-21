from .models import Page
from django import forms
# from django.utils import timezone

# from pagedown.widgets import PagedownWidget
from django_summernote.widgets import SummernoteWidget


class PageForm(forms.ModelForm):

    body = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Page
        fields = ('title',
                  'show_title',
                  'slug',
                  'header_image',
                  'body'
                  )
    '''
    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')

        return publish_date
    '''