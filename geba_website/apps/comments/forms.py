from django import forms
# from .models import Comment
# from markdownx.fields import MarkdownxFormField


class CommentForm(forms.Form):

    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea)
    # content = MarkdownxFormField()

    # class Meta:
    #     model = Comment
    #     fields = ('content',
    #               )
