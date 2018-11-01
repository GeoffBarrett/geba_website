from .models import Post
from django import forms
# from django.utils import timezone

# from pagedown.widgets import PagedownWidget
from django_summernote.widgets import SummernoteWidget


class BlogPostForm(forms.ModelForm):

    publish_date = forms.DateTimeField(widget=forms.SelectDateWidget)
    body = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '480'}}))

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