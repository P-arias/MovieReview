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

API_KEY = '444422-MovieRev-XMHI8X3L'
def index(request):

        search = 'Marvel'

        form = SearchForm(request.POST or None)
        if form.is_valid():
            form.save()

        if request.method == 'POST':
            search = request.POST.get('term')
            search = search.strip()



        #response = requests.get('https://tastedive.com/api/similar?q=' + search + '&type=movies&info=1&limit=20&k=' + API_KEY)
        #data = response.json()
        #movies = data['Similar']['Info']
        #movies.extend(data['Similar']['Results'])

       # for movie in movies:
          #  responseImages = requests.get('https://serpapi.com/playground?q=titanicmovie&tbm=isch&ijn=0')
          #  imageSearch = responseImages.json()
           # movie['wUrl'] = imageSearch['images_results']['thumbnail']


        url = "https://moviesdb5.p.rapidapi.com/om"

        querystring = {"s": search, "type": "movie", "r": "json"}

        headers = {
            "X-RapidAPI-Key": "f971ebd360mshca57000ed7260fbp131452jsn0c465236876d",
            "X-RapidAPI-Host": "moviesdb5.p.rapidapi.com"
        }

        searchTerms = ['']
        if request.user.is_authenticated:
            try:
                searchTerms = SearchTerms.objects.filter(userId_id=request.user.id)

            except ObjectDoesNotExist:
                searchTerms = ['']
                pass

        response = requests.request("GET", url, headers=headers, params=querystring)
        movies = response.json()
        context = {'movies': movies['Search'], 'searchTerms': searchTerms, 'form': form}
        return render(request, 'review/index.html', context)

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

    url = "https://moviesdb5.p.rapidapi.com/om"

    querystring = {"i": movie_id}

    headers = {
        "X-RapidAPI-Key": "f971ebd360mshca57000ed7260fbp131452jsn0c465236876d",
        "X-RapidAPI-Host": "moviesdb5.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    movie = response.json()
    context = {'movie': movie, 'posts': posts_results}
    return render(request, 'review/posts.html', context)

@login_required(login_url='login')
def add(request, movie_id, user_name, movie_title):
    # Create a form instance and populate it with data from the request
    form = PostForm(request.POST or None)

    if form.is_valid():
        print('sucess')
        # save the record into the db
        form.save()
        # after saving redirect to view_product page
        return posts(request, movie_id)
    print('fail')
    # if the request does not have post data, a blank form will be rendered
    return render(request, 'review/add.html', {'form': form, 'movie_id': movie_id, 'movie_title': movie_title})

@login_required(login_url='login')
def update(request, post_id, user_name, redirect):
    # Get the product based on its id

    post = Post.objects.get(id=post_id, authorId=request.user)
    # populate a form instance with data from the data on the database
    # instance=product allows to update the record rather than creating a new record when save method is called
    form = PostForm(request.POST or None, instance=post)

    # check whether it's valid:
    #if post.authorId_id == request.user.id:
    if form.is_valid():
        print('success 1')
        # update the record in the db
        form.save()
        print('success 2')
        # after updating redirect to view_product page
        if(redirect == 'account'):
            return account(request)
        elif(redirect == 'posts'):
            return posts(request, post.movieId)
    #else:
      #  return index(request)

    # if the request does not have post data, render the page with the form containing the product's info
    return render(request, 'review/update.html', {'form': form, 'post_id': post_id, 'post': post, 'redirect': redirect})

@login_required(login_url='login')
def delete(request, post_id, user_name, redirect):
    # Get the product based on its id
    post = Post.objects.get(id=post_id)
    # if this is a POST request, we need to delete the form data
    if post.authorId_id == request.user.id:
        post.delete()
        # after deleting redirect to view_product page
        if (redirect == 'account'):
            return account(request)
        elif (redirect == 'posts'):
            return posts(request, post.movieId)
    else:
        return index(request)

@login_required(login_url='login')
def account(request):

    posts_results = Post.objects.filter(author__icontains=request.user.username)
    context = {'posts': posts_results}
    return render(request, 'review/account.html', context)


def searchTerms(request):

    if request.is_ajax and request.method == "POST":

        search_results = SearchTerms.objects.filter(userId=request.POST.get('userId'))
        ser_instance = serializers.serialize('json', [search_results, ])
        # send to client side.
        return JsonResponse({"instance": ser_instance}, status=200)
