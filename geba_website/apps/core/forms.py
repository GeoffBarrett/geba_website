# from django.contrib.auth.models import User
from .models import User
from django import forms
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Password'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Re-Type Password'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            existing_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username.lower()
        raise forms.ValidationError("Your username must be unique!")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            existing_email = User.objects.get(email=email)
        except User.DoesNotExist:
            return email.lower()
        raise forms.ValidationError("Your e-mail must be unique!")

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
'''
class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            raise forms.ValidationError("You have not entered in a password!")

    def clean_username(self):

        username = self.cleaned_data.get('username')

        return username.lower()
'''


class LoginForm(forms.Form):

    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
