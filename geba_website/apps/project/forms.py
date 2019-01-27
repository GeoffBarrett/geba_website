from .models import ProjectPost, Project
from django import forms
# from django.contrib.admin.widgets import AdminSplitDateTime, AdminDateWidget
# from django.utils import timezone
# from pagedown.widgets import PagedownWidget
from tinymce.widgets import TinyMCE
# from django_summernote.widgets import SummernoteWidget


class ProjectPostForm(forms.ModelForm):

    # this prefix will put the value before the name so that conflicting element names won't cause errors
    prefix = 'post'

    # publish_date = forms.DateTimeField(widget=forms.SelectDateWidget(show_preview=False))
    publish_date = forms.DateTimeField(widget=forms.SelectDateWidget)

    # publish_date = forms.DateTimeField(widget=AdminSplitDateTime())
    # publish_date = forms.DateInput(attrs={'class': 'date_picker'})

    # body = forms.CharField(widget=PagedownWidget())  # this is for pagedown wysiwyg
    # body = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '480'}}))
    body = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'}))

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
        widgets = {
            'body': SummernoteInplaceWidget(),
        }'''


class ProjectForm(forms.ModelForm):

    # prefix = 'project'

    publish_date = forms.DateTimeField(widget=forms.SelectDateWidget)

    # body = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '480'}}),
    #                        required=False)

    body = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'}), required=False)

    class Meta:

        model = Project
        fields = ('title',
                  'body',
                  'image',
                  'image_caption',
                  'publish_date',
                  'draft',
                  )
