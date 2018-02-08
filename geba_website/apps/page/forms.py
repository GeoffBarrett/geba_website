from .models import Page
from django import forms


class PagePostForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ('title',
                  'subtitle',
                  'body',
                  'image',
                  'image_caption',
                  'draft',
                  'publish_date',
                  )