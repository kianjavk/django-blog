from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth import login , logout ,authenticate
from django.views.generic import View
from .forms import  CustomerUserCreationForm,UserLoginForm,UserUpdateForm
from .models import CustomerUser,

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class UserRegisterView(View):
    form_class = CustomerUserCreationForm
    template_name = 'accounts/register/signup.html'
    success_url = reverse_lazy('home_page')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = CustomerUser(
                email=cd['email'],
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                birthdate=cd['birthdate']
            )
            user.set_password(cd['password1'])
            user.save()
            messages.success(request, 'Your account has been created!', 'success')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

#       User Login
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login/login.html'
    success_url = reverse_lazy('accounts:')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in!', 'success')
                return redirect('home_page')
            messages.error(request, ' email or password is wrong!', 'danger')
        return render(request, self.template_name, {'form': form})


#       User Logout
class UserLogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('home_page')


class UserProfileView(LoginRequiredMixin,View):

    def get(self, request,user_id):
        user = CustomerUser.objects.get(pk=user_id)
        print(f"User: {user}")
        return render(request,'customer/profile.html',{'user':user})

class UpdateProfileView(LoginRequiredMixin,View):
    form_class = UserUpdateForm
    template_name = 'customer/update.html'
    success_url = reverse_lazy('customer/profile.html')

    def get(self, request,user_id):
        user = CustomerUser.objects.get(pk=user_id)
        form = self.form_class(instance=user)

        return render(request, self.template_name, {'form': form})

    def post(self,request,user_id):
        user = CustomerUser.objects.get(pk=user_id)
        form = self.form_class(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!', 'success')

        return render(request, self.template_name, {'form': form})
