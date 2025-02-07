from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomerUser
from django.core.exceptions import ValidationError


class CustomerUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = ('first_name', 'last_name', 'email', 'birthdate')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match")
        return cd['password2']

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomerUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you cant change password using <a href="../password/">this form</a>.')

    class Meta:
        model = CustomerUser
        fields = ('first_name', 'last_name', 'email', 'password', 'birthdate','last_login')


#       User Register

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')
    birthdate = forms.DateField(label='Birthdate')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='confirm Password', widget=forms.PasswordInput())

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        return cd['password2']


    def clean_email(self):
        email = self.cleaned_data['email']
        user = CustomerUser.objects.filter(email=email)
        if user:
            raise ValidationError("This email already exists")
        return email


#     User Update

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = ['first_name','last_name','email','birthdate']



    def clean_email(self):
        email = self.cleaned_data['email']
        user = CustomerUser.objects.filter(email=email)
        if user:
            raise ValidationError("this Email already exists")
        return email


#       User Login

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

