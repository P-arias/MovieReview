from django.shortcuts import render, redirect
import json
import requests
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

API_KEY = '444422-MovieRev-XMHI8X3L'
def index(request):

        search = 'Marvel'
        if request.method == 'POST':
            search = request.POST.get('search')
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

        response = requests.request("GET", url, headers=headers, params=querystring)
        movies = response.json()
        context = {'movies': movies['Search']}
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