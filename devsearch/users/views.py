from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User  # the default user model for auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm
# Create your views here.


def loginUser(request):
    page = 'login'
    context = {"page": page}

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

    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)  # deletes the session
    messages.success(request, 'User was successfully logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        # just like model forms
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # form.save() - hold the commit for some validations
            user = form.save(commit=False)

            # we want to ensure that the username is all lowercase
            user.username = user.username.lower()
            user.save()

            # display a flash message
            messages.success(request, 'User successfully registered')

            # also log in the user rightaway, we already have the user instance
            login(request, user)  # creates a session
            return redirect('edit-account')

        else:
            messages.error(request, "Error occured during registration")

    context = {"page": page, "form": form}

    return render(request, 'users/login_register.html', context)


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


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    # request.user is the logged in user
    # profile is the one-to-one relationship of the user
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, "skills": skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=profile)
        if form.is_valid:
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('account')

        else:
            messages.error(request, 'Some error occured')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)
