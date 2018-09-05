# from django.shortcuts import render
from .forms import UserCreationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
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
from django.urls import reverse_lazy
# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('pages:home')


class LoginFormView(FormView):

    form_class = LoginForm
    template_name = 'geba_auth/signin_form.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        register_form = UserCreationForm()

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # can now refer to them as request.geba_auth.username

            return super(LoginFormView, self).form_valid(form)

        else:
            return render(request, self.template_name, {'login_form': form, 'register_form': register_form})


class RegisterFormView(FormView):

    form_class = UserCreationForm
    template_name = 'geba_auth/register_form.html'
    success_url = reverse_lazy('geba_auth:account_activation_sent')

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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)

            return super(RegisterFormView, self).form_valid(form)

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
        return render(request, 'account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'geba_auth/account_activation_sent.html')


def account_activation_invalid(request):
    return render(request, 'geba_auth/account_activation_invalid.html')
