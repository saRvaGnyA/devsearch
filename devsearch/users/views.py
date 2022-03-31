from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User  # the default user model for auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
# Create your views here.


def loginUser(request):
    # DO NOT CALL THIS FUNCTION `login` since we'd use Django's built-in authentication login function with the same name ahead

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # first verify the form fields
        try:
            # user exists?
            user = User.objects.get(username=username)
        except:
            # we'll display a flash message to the user later
            messages.error(request, 'Username does not exist')

        # now that the user exists, authenticate the user
        user = authenticate(request, username=username, password=password)
        # This method returns
        # 1. the User instance if password matches
        # 2. `None` object if authentication fails

        if user is not None:
            # this creates a session in the DB, and adds the session ID in the browser cookie
            login(request, user)
            return redirect('profiles')

        else:
            # we'll display a flash message to the user later
            messages.error(request, 'Username OR password do not match')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)  # deletes the session
    messages.success(request, 'User was successfully logged out')
    return redirect('login')


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description__exact="")
    context = {"profile": profile, "top_skills": top_skills,
               "other_skills": other_skills}
    return render(request, 'users/user-profile.html', context)
