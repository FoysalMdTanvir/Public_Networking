from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from App_Login.models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='',
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(required=True, label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(required=True, label='',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class UserLogin(AuthenticationForm):
    username = forms.CharField(required=True, label='',
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(required=True, label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileChange(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class ProfilePic(forms.ModelForm):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', }))

    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'dob', 'description', 'website')
