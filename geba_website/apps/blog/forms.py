from .models import Post
from django import forms
# from django.utils import timezone

from pagedown.widgets import PagedownWidget


class BlogPostForm(forms.ModelForm):

    publish_date = forms.DateTimeField(widget=forms.SelectDateWidget)
    body = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Post
        fields = ('title',
                  'body',
                  'image',
                  'image_caption',
                  'draft',
                  'publish_date',
                  )
    '''
    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')

        return publish_date
    '''