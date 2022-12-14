from django.shortcuts import render, redirect
import json
import requests
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .forms import PostForm
from .models import Post
from .forms import SearchForm
from .models import SearchTerms
from django.http import JsonResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist


def index(request):


    search = 'Marvel'

    # Avoid saving the same keyterm for the same user more than once
    form = SearchForm(request.POST or None)
    if form.is_valid():
        duplicate = SearchTerms.objects.filter(userId_id=request.user.id, term__icontains=request.POST.get('term'))
        if not duplicate:
            form.save()

    if request.method == 'POST':
        search = request.POST.get('term')
        search = search.strip()

    querystring = {"s": search, "type": "movie", "r": "json"}

    searchTerms = ['']
    if request.user.is_authenticated:
        try:
            searchTerms = SearchTerms.objects.filter(userId_id=request.user.id)

        except ObjectDoesNotExist:
            searchTerms = ['']
            pass

    response = getDataFromAPI(querystring)
    movies = response.json()
    try:
        context = {'movies': movies['Search'], 'searchTerms': searchTerms, 'form': form}
    except KeyError:
        movies = [{'Poster': '#', 'Title': 'Movie not found try again', 'Year': '', 'imdbID': 'tt4154664'}]
        context = {'movies': movies, 'searchTerms': searchTerms, 'form': form}
    return render(request, 'review/index.html', context)


def getDataFromAPI(querystring):

    url = "https://moviesdb5.p.rapidapi.com/om"

    headers = {
        "X-RapidAPI-Key": "#",
        "X-RapidAPI-Host": "moviesdb5.p.rapidapi.com"
    }

    return requests.request("GET", url, headers=headers, params=querystring)

def register_view(request):
    # This function renders the registration form page and create a new user based on the form data
    if request.method == 'POST':
        # We use Django's UserCreationForm which is a model created by Django to create a new user.
        # UserCreationForm has three fields by default: username (from the user model), password1, and password2.
        # If you want to include email as well, switch to our own custom form called UserRegistrationForm
        form = UserCreationForm(request.POST or None)
        # check whether it's valid: for example it verifies that password1 and password2 match
        if form.is_valid():
            # form.save()
            # if you want to log in the user directly after registration, use the following three lines,
            # which logins the user and redirect to index
            user = form.save()
            login(request, user)
            return redirect('index')
            # if you do want to log in the user directly after registration, comment out the three lines above,
            # redirect the user to login page so that after registration the user can enter the credentials
            # return redirect('login')
    else:
        # Create an empty instance of Django's UserCreationForm to generate the necessary html on the template.
        form = UserCreationForm()

    return render(request, 'review/register.html', {'form': form})


def login_view(request):
    # this function authenticates the user based on username and password
    # AuthenticationForm is a form for logging a user in.
    # if the request method is a post
    if request.method == 'POST':
        # Plug the request.post in AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the user info from the form data and login the user
            user = form.get_user()
            login(request, user)
            # redirect the user to index page
            return redirect('index')
    else:
        # Create an empty instance of Django's AuthenticationForm to generate the necessary html on the template.
        form = AuthenticationForm()

    return render(request, 'review/login.html', {'form': form})


def logout_view(request):
    # This is the method to log out the user
    logout(request)
    # redirect the user to index page after logout
    return redirect('index')

def posts(request, movie_id):

    posts_results = Post.objects.filter(movieId__icontains=movie_id)

    querystring = {"i": movie_id}

    response = getDataFromAPI(querystring)
    movie = response.json()

    searchTerms = ['']
    if request.user.is_authenticated:
        try:
            searchTerms = SearchTerms.objects.filter(userId_id=request.user.id)

        except ObjectDoesNotExist:
            searchTerms = ['']
            pass

    context = {'movie': movie, 'posts': posts_results, 'searchTerms': searchTerms}
    return render(request, 'review/posts.html', context)

@login_required(login_url='login')
def add(request, movie_id):
    # Create a form instance and populate it with data from the request
    form = PostForm(request.POST or None)

    if form.is_valid():
        # save the record into the db
        form.save()
        # after saving redirect to view_product page
        return posts(request, movie_id)
    # if the request does not have post data, error
    return render(request, 'review/error.html')

@login_required(login_url='login')
def update(request, post_id, redirect):
    # Get the product based on its id
    try:
        post = Post.objects.get(id=post_id, authorId=request.user)
    except ObjectDoesNotExist:
        return render(request, 'review/error.html')
    # populate a form instance with data from the data on the database
    # instance=product allows to update the record rather than creating a new record when save method is called
    form = PostForm(request.POST or None, instance=post)

    # check whether it's valid:
    #if post.authorId_id == request.user.id:
    if form.is_valid():
        # update the record in the db
        form.save()
        # after updating redirect to view_product page
        if(redirect == 'account'):
            return account(request)
        elif(redirect == 'posts'):
            return posts(request, post.movieId)
    #else:
      #  return index(request)

    # if the request does not have post data, render the page with the form containing the product's info
    searchTerms = ['']
    if request.user.is_authenticated:
        try:
            searchTerms = SearchTerms.objects.filter(userId_id=request.user.id)

        except ObjectDoesNotExist:
            searchTerms = ['']
            pass
        context = {'form': form, 'post_id': post_id, 'post': post, 'redirect': redirect, 'searchTerms': searchTerms}
    return render(request, 'review/update.html', context)

@login_required(login_url='login')
def delete(request, post_id, redirect):
    # Get the post based on its id
    try:
        post = Post.objects.get(id=post_id, authorId=request.user)
    except ObjectDoesNotExist:
        return render(request, 'review/error.html')
    post.delete()
    # after deleting redirect to the page from where the request came from
    if (redirect == 'account'):
        return account(request)
    elif (redirect == 'posts'):
        return posts(request, post.movieId)

    return render(request, 'review/error.html')

@login_required(login_url='login')
def account(request):

    searchTerms = ['']
    if request.user.is_authenticated:
        try:
            searchTerms = SearchTerms.objects.filter(userId_id=request.user.id)

        except ObjectDoesNotExist:
            searchTerms = ['']
            pass

    posts_results = Post.objects.filter(authorId=request.user)
    context = {'posts': posts_results, 'searchTerms': searchTerms}
    return render(request, 'review/account.html', context)

def error(request):
    return  render(request, 'review/error.html')