# from django.shortcuts import render
from .forms import UserCreationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import FormView
# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('core:index')


class LoginFormView(FormView):

    form_class = LoginForm
    template_name = 'geba_auth/signin_form.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):

        # form = self.form_class(request.POST)
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
    # template_name = 'geba_auth/signin_form.html'
    template_name = 'geba_auth/register_form.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):

        login_form = LoginForm()
        form = self.form_class(request.POST)
        # print(form)
        if form.is_valid():

            user = form.save(commit=False)  # creates object from the form, doesn't save it to the database just yet

            # normalize the data so everything is in the same format
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            user.set_password(password)  # saves the hashed password
            user.save()  # saves the information

            # authenticate the geba_auth
            user = authenticate(username=username, password=password)

            if user is not None:
                '''if authenticated it returns the geba_auth variable (none otherwise)'''

                if user.is_active:
                    '''checks to make sure the account is not banned or anything'''
                    login(request, user)  # can now refer to them as request.geba_auth.username
            return super(RegisterFormView, self).form_valid(form)

        else:
            return render(request, self.template_name, {'login_form': login_form, 'register_form': form})
