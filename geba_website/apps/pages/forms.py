from .models import Page
from django import forms
# from django.utils import timezone

# from pagedown.widgets import PagedownWidget
from django_summernote.widgets import SummernoteWidget


class PageForm(forms.ModelForm):

    body = forms.CharField(widget=SummernoteWidget(), required=False)

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


class ContactForm(forms.Form):
    contact_first_name = forms.CharField(required=True, label='First Name')
    contact_last_name = forms.CharField(required=True, label='Last Name')
    contact_email = forms.EmailField(required=True, label='E-Mail')

    contact_content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label='Message'
    )
