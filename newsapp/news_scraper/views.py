from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User, UserProfile


# Create your views here.

@login_required()
def user_home(request):
    if request.user.is_authenticated and request.user.is_active:
        context = {'user': request.user}
        return render(request, 'news_scraper/user_home.html',context)

@login_required
def user_tags(request):
    if request.user.is_authenticated and request.user.is_active:
        context = {'user': request.user}
        return render(request, 'news_scraper/user_tags.html',context)

@login_required()
def user_sources(request):
    if request.user.is_authenticated and request.user.is_active:
        context = {'user': request.user}
        return render(request, 'news_scraper/user_sources.html',context)   
             
def guest_home(request):
    if request.user != None and request.user.is_authenticated and request.user.is_active:
        return HttpResponseRedirect(reverse('news_scraper:user_home'))
    return render(request, 'news_scraper/guest_home.html')    

def user_login(request):
    # if is post method check for relevant data
    if request.method == 'POST':
        # get username and password.
        # use the POST.get method so it returns None 
        # instead of erroring if field left empty
        username = request.POST.get('username')
        password = request.POST.get('password')  

        # check whether user exists in DB
        user = authenticate(username=username, password=password)
        # will return None if doesn't exist

        if user:
            if user.is_active:
                # valid and active
                login(request, user) 
                return HttpResponseRedirect(reverse('news_scraper:user_home'))               
            else:
                return HttpResponse("This account has been disabled.")
        else:
            print("Invalid login credentials: {0}, ***".format(username))
            return HttpResponse("Invalid login details supplied")    
    else:
        # not a POST method so supply login form if not logged in
        # if logged in, go straight to user home
        if request.user != None and request.user.is_authenticated and request.user.is_active:
            return HttpResponseRedirect(reverse('news_scraper:user_home'))
        return render(request, 'news_scraper/login.html')

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('news_scraper:guest_home'))

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