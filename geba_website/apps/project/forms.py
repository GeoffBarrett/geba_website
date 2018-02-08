from .models import ProjectPost, Project
from django import forms
from django.utils import timezone

from pagedown.widgets import PagedownWidget


class ProjectPostForm(forms.ModelForm):

    # this prefix will put the value before the name so that conflicting element names won't cause errors
    prefix = 'post'

    # publish_date = forms.DateTimeField(widget=forms.SelectDateWidget(show_preview=False))
    publish_date = forms.DateTimeField(widget=forms.SelectDateWidget)
    body = forms.CharField(widget=PagedownWidget())

    class Meta:
        model = ProjectPost
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


class ProjectForm(forms.ModelForm):

    # prefix = 'project'

    publish_date = forms.DateTimeField(widget=forms.SelectDateWidget)

    class Meta:

        model = Project
        fields = ('title',
                  'image',
                  'image_caption',
                  'publish_date',
                  'draft',
                  )
