from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet

from .models import User, UserProfile, Source, Tag


# Create your views here.

@login_required()
def user_home(request):
    if request.user.is_authenticated and request.user.is_active:
        context = {'user': request.user}
        return render(request, 'news_scraper/user_home.html', context)


@login_required
def user_tags(request):
    if request.user.is_authenticated and request.user.is_active:

        profile = request.user.userprofile

        if request.method == 'POST':

            tag_name = request.POST.get('tag')

            try:
                add_tag = Tag.objects.get(name=tag_name)
                add_tag.adds += 1
            except:
                add_tag = Tag(name=tag_name, adds=1)

            add_tag.save()

            profile.tags_list.add(add_tag)
            profile.save()

            return HttpResponseRedirect(reverse('news_scraper:user_tags'))

        else:

            user_tags = profile.tags_list.all()
            print(user_tags)
            all_tags = Tag.objects.all()
            print(all_tags)
            popular_tags = all_tags.difference(user_tags)
            print(popular_tags)
            """for tag in popular_tags:
                if tag in user_tags or tag.adds <= 0:
                    popular_tags.remove(tag)"""
            popular_tags = popular_tags[:5]

            context = {
                'user': request.user,
                'user_tags': user_tags,
                'popular_tags': popular_tags
            }
            return render(request, 'news_scraper/user_tags.html', context)


@login_required()
def user_sources(request):
    if request.user.is_authenticated and request.user.is_active:

        profile = request.user.userprofile

        user_sources = profile.sources_list.all().order_by('-name')
        new_sources = Source.objects.order_by('-name')

        for src in new_sources:
            if src in user_sources:
                new_sources.remove(src)

        context = {
            'user': request.user,
            'user_sources': user_sources,
            'new_sources': new_sources
        }
        return render(request, 'news_scraper/user_sources.html', context)


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

    # render the template
    options = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        'username': username
    }

    return render(request, 'news_scraper/register_new_user.html', options)
