# from django.shortcuts import render
from .forms import UserCreationForm, LoginForm, ResendEmailForm, ForgotPasswordForm, ResetPasswordForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from ..geba_auth.models import User
from django.utils.http import urlsafe_base64_decode
# from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
# Create your views here.
from .signals import user_logged_in


def logout_view(request):
    logout(request)
    return redirect('pages:home')


class LoginFormView(FormView):

    form_class = LoginForm
    template_name = 'geba_auth/signin_form.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = form.login(request)

            if user is not None:
                login(request, user)  # can now refer to them as request.geba_auth.username
                user_logged_in.send(user.__class__, instance=user, request=request)
                return HttpResponseRedirect('/')
            else:
                return render(request, self.template_name, {'form': form})

        else:
            return render(request, self.template_name, {'form': form})


class RegisterFormView(FormView):

    form_class = UserCreationForm
    template_name = 'geba_auth/register_form.html'

    def post(self, request, *args, **kwargs):

        # login_form = LoginForm()
        form = self.form_class(request.POST)
        # print(form)
        if form.is_valid():

            user = form.save(commit=False)  # creates object from the form, doesn't save it to the database just yet

            user.is_active = False

            # normalize the data so everything is in the same format
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            user.set_password(password)  # saves the hashed password
            user.save()  # saves the information

            current_site = get_current_site(self.request)
            subject = 'Activate Your GEBA Account!'
            message = render_to_string('geba_auth/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)

            previous_url = request.META.get('HTTP_REFERER')

            if previous_url:
                url_split = previous_url.split('/')

                if url_split[-2] == 'register' and url_split[-3] == 'auth':
                    # then we were on the registration page, route back to the home page
                    previous_url = '/'

                self.success_url = previous_url + '#activation_sent'
            else:
                pass

            return HttpResponseRedirect(self.success_url)

        else:
            return render(request, self.template_name, {'form': form})


class ResendActivationFormView(FormView):

    form_class = ResendEmailForm
    template_name = 'geba_auth/resend_email_form.html'

    def post(self, request, *args, **kwargs):

        # login_form = LoginForm()
        form = self.form_class(request.POST)
        # print(form)
        if form.is_valid():

            email = form.cleaned_data['email']

            user = User.objects.get(email=email)

            if user:
                current_site = get_current_site(self.request)
                subject = 'Activate Your GEBA Account!'
                message = render_to_string('geba_auth/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                user.email_user(subject, message)

                previous_url = request.META.get('HTTP_REFERER')

                if previous_url:
                    url_split = previous_url.split('/')

                    if url_split[-2] == 'register' and url_split[-3] == 'auth':
                        # then we were on the registration page, route back to the home page
                        previous_url = '/'

                    self.success_url = previous_url + '#activation_sent'
                else:
                    pass
            else:
                self.success_url = self.request

            return HttpResponseRedirect(self.success_url)

        else:
            return render(request, self.template_name, {'form': form})


class ForgotPasswordFormView(FormView):
    """Filling out this form will send a link to the user so that they can reset the password for their account"""
    form_class = ForgotPasswordForm
    template_name = 'geba_auth/forgot_password.html'

    def post(self, request, *args, **kwargs):

        # login_form = LoginForm()
        form = self.form_class(request.POST)
        # print(form)
        if form.is_valid():

            email = form.cleaned_data['email']

            user = User.objects.get(email=email)

            if user:
                current_site = get_current_site(self.request)
                subject = 'GEBA Account: Password Reset!'
                message = render_to_string('geba_auth/forgot_password_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })

                user.email_user(subject, message)

                previous_url = request.META.get('HTTP_REFERER')

                if previous_url:
                    url_split = previous_url.split('/')

                    if url_split[-2] == 'forgot_password' and url_split[-3] == 'auth':
                        # then we were on the registration page, route back to the home page
                        previous_url = '/'

                    self.success_url = previous_url + '#reset_sent'
                else:
                    pass
            else:
                self.success_url = self.request

            return HttpResponseRedirect(self.success_url)

        else:
            return render(request, self.template_name, {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('pages:home')
    else:
        return render(request, 'geba_auth/account_activation_invalid.html')


class reset_password(FormView):
    form_class = ResetPasswordForm
    template_name = 'geba_auth/reset_password.html'

    def post(self, request, *args, **kwargs):

        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        form = self.form_class(request.POST)

        if user is not None and account_activation_token.check_token(user, token):
            if form.is_valid():
                user.set_password(form.cleaned_data["password1"])
                user.save()

                login(request, user)
                return redirect('pages:home')
            else:
                return render(request, self.template_name, {'form': form, 'uid': uidb64, 'token': token})
        else:
            return render(request, 'geba_auth/reset_password_invalid.html')

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        uidb64 = kwargs['uidb64']
        token = kwargs['token']

        form = self.form_class()

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            return render(request, self.template_name, {'form': form, 'uid': uidb64, 'token': token})
        else:
            return render(request, 'geba_auth/reset_password_invalid.html')


def account_activation_sent(request):
    return render(request, 'geba_auth/account_activation_sent.html')


def account_activation_invalid(request):
    return render(request, 'geba_auth/account_activation_invalid.html')
