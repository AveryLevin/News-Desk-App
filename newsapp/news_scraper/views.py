from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import User, UserProfile

# Create your views here.

def user_home(request, user_name):
    user = get_object_or_404(User, username=user_name)
    if user != Http404:
        profile = user.userprofile
        return HttpResponse("USER HOME (not implemented). " + user_name + " exists.")
    else:
        return Http404("could not find specified user")

def register_new_user(request):
    # gives status of registration
    registered = False

    username = None
    # if user is posting data, check forms for info
    if request.method == 'POST':
        # read raw data from forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # check if forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save data to database
            user = user_form.save()

            # hash password
            user.set_password(user.password)
            # update saved user
            user.save()

            # create a UserProfile instance. 
            # Don't commit to DB yet to add attributes
            profile = profile_form.save(commit=False)
            profile.user = user

            # now save profile
            profile.save()

            # save username for redir
            username = user.username

            # update state var
            registered = True
        else: 
            # dump error log
            print(user_form.errors, profile_form.errors)
    else:
        # Not a POST method.
        # render the form using two ModelForm instances
        user_form = UserForm()
        profile_form = UserProfileForm()

    #render the template
    options = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        'username': username
    }

    return render(request, 'news_scraper/register_new_user.html', options)