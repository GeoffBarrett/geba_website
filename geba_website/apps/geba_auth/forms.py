# from django.contrib.geba_auth.models import User
from .models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Use a valid email address.')
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Password'),
                                help_text='Required. Passwords must have at least 8 characters!')
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Re-Type Password'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Password must have at least 8 characters!")

        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")

        if len(password2) < 8:
            raise forms.ValidationError("Password must have at least 8 characters!")

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


class LoginForm(forms.Form):

    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            existing_user = User.objects.get(username=username)
            if not existing_user.email_confirmed and not existing_user.is_superuser:
                raise forms.ValidationError(mark_safe("E-mail not confirmed, <a href='%s'>Resend Activation</a>!" % (reverse_lazy('geba_auth:resend_act'))))

        except User.DoesNotExist:
            raise forms.ValidationError("Username does not exist!")
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        try:
            existing_user = User.objects.get(username=username)
            if not existing_user.email_confirmed:
                return password
        except User.DoesNotExist:
            return password

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError(mark_safe("Invalid Password!, <a href='%s'>Forgot Password</a>?" % (reverse_lazy('geba_auth:forgot_password'))))
        elif not user.is_active:
            raise forms.ValidationError("User not active!")

        return password

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        return user


class ResendEmailForm(forms.Form):

    email = forms.EmailField(max_length=254, help_text='Required. Use a valid email address.')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            existing_user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise forms.ValidationError("This e-mail does not belong to a user!")
        return email


class ResetPasswordForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label=_('Password'),
                                help_text='Required. Passwords must have at least 8 characters!')
    password2 = forms.CharField(widget=forms.PasswordInput, label=_('Re-Type Password'))

    class Meta:
        model = User
        fields = ('password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Password must have at least 8 characters!")

        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")

        if len(password2) < 8:
            raise forms.ValidationError("Password must have at least 8 characters!")

        return password2


class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(max_length=254, help_text='Required. Use a valid email address.')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            existing_user = User.objects.get(email=email)

        except User.DoesNotExist:
            raise forms.ValidationError("This e-mail does not belong to a user!")
        return email
