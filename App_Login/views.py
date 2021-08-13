from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.forms import SignUpForm, UserLogin, UserProfileChange, ProfilePic
from App_Login.models import UserProfile, Follow
from django.contrib.auth.models import User
# Create your views here.


def sign_up(request):
    form = SignUpForm()
    registered = False
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True
    dict = {'form': form, 'registered': registered}
    return render(request, 'App_Login/signup.html', context=dict)


def login_page(request):
    form = UserLogin()
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    return render(request, 'App_Login/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    return render(request, 'App_Login/profile.html', context={})


'''Old user_change function'''
# @login_required
# def user_change(request):
#     current_user = request.user
#     form = UserProfileChange(instance=current_user)
#     if request.method == 'POST':
#         form = UserProfileChange(request.POST, instance=current_user)
#         if form.is_valid():
#             form.save()
#             form = UserProfileChange(instance=current_user)
#     return render(request, 'App_Login/change_profile.html', context={'form': form})

'''Updated user_change function'''
# user profile updated


@login_required
def user_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    profile_form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        profile_form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            form = UserProfileChange(instance=current_user)
    return render(request, 'App_Login/change_profile.html', context={'form': form, 'profile_form': profile_form})


@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'App_Login/change_pass.html', context={'form': form, 'changed': changed})


@login_required
def add_pro_pic(request):
    form = ProfilePic()
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user = request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html', context={'form': form})


@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro_pic_add.html', context={'form': form})


@login_required
def user(request, username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/user_other.html', context={'user_other': user_other, 'already_followed': already_followed})


@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username': username}))


@login_required
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('App_Login:user', kwargs={'username': username}))
