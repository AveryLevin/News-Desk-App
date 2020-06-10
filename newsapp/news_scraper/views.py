from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.views.decorators.csrf import csrf_exempt

from .models import User, UserProfile, Source, Tag
from .scraper_module import SourceScraper

import json

# Create your views here.


@login_required()
def user_home(request):
    if request.user.is_authenticated and request.user.is_active:

        profile = request.user.userprofile
        sources = list(profile.sources_list.all())
        tags = list(profile.tags_list.all())

        articles = []
        if sources and tags:
            # if user has sources and tags saved, the page should load current articles

            for source in sources:
                scraper = SourceScraper(source=source, tags=tags)
                articles.extend(scraper.parse())

        articles = dictify('articles', articles)
        context = {
            'user': request.user,
            'articles_json': {
                'articleListData': articles
            }
        }
        return render(request, 'news_scraper/user_home.html', context)


def dictify(m_arg: str, m_list: list) -> list:
    if m_arg == 'articles':
        articles = m_list
        if articles:
            articles_list = []

            for article in articles:
                article_dict = {
                    "title": article.title,
                    "source": article.source,
                    "redir": article.redir
                }
                articles_list.append(article_dict)

            return articles_list
    elif m_arg == 'sources':
        sources = m_list
        if sources:
            sources_list = []

            for source in sources:
                source_dict = {
                    "name": source.name
                }
                sources_list.append(source_dict)

            return sources_list
    return None


@login_required
def user_tags(request):
    if request.user.is_authenticated and request.user.is_active:

        profile = request.user.userprofile

        if request.method == 'POST':

            action = request.POST.get('action')
            tag_name = request.POST.get('tag-name')
            print(":::", type(tag_name))
            if action == 'Add' or action == 'Add Tag':
                try:
                    tag = Tag.objects.get(name=tag_name)
                    tag.adds += 1
                except:
                    tag = Tag(name=tag_name, adds=1)

                tag.save()
                profile.tags_list.add(tag)

            elif action == 'Delete Tag':
                try:
                    tag = Tag.objects.get(name=tag_name)
                    tag.adds -= 1
                except:
                    return Http404("Couldn't find Tag")

                tag.save()
                profile.tags_list.remove(tag)

            profile.save()

            return HttpResponseRedirect(reverse('news_scraper:user_tags'))

        else:

            user_tags = profile.tags_list.all()

            all_tags = Tag.objects.all()

            popular_tags = all_tags.difference(user_tags).order_by('-adds')

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


@csrf_exempt
@login_required()
def user_sources(request):
    if request.user.is_authenticated and request.user.is_active:

        profile = request.user.userprofile

        if request.method == 'POST':
            data = request.body
            if data:
                data = json.loads(data)
                print(data)

                action = data.get('action')
                source_name = data.get('name')
                print(action)
                print(source_name)
                if action == 'Add Source':
                    try:

                        source = Source.objects.get(name=source_name)
                        profile.sources_list.add(source)
                    except:
                        print("Couldn't find source to add.")
                        return Http404("Couldn't find source.")

                elif action == 'Remove Source':
                    try:
                        source = profile.sources_list.get(name=source_name)
                        profile.sources_list.remove(source)
                    except:
                        print("Couldn't find source to remove.")
                        return Http404("Couldn't find source.")
                profile.save()

                user_sources = profile.sources_list.all()
                all_sources = Source.objects.all()
                new_sources = all_sources.difference(
                    user_sources).order_by('-name')

                user_sources = dictify('sources', user_sources)
                new_sources = dictify('sources', new_sources)

                context = {
                    'sourceData': {
                        'currentSources': user_sources,
                        'additionalSources': new_sources
                    }
                }

                return JsonResponse(data=context)
            else:
                return JsonResponse(data={})
        else:
            user_sources = profile.sources_list.all()
            all_sources = Source.objects.all()
            new_sources = all_sources.difference(
                user_sources).order_by('-name')

            user_sources = dictify('sources', user_sources)
            new_sources = dictify('sources', new_sources)

            context = {
                'user': request.user,
                'sourceData': {
                    'currentSources': user_sources,
                    'additionalSources': new_sources
                }
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
