from django.shortcuts import render, redirect
import json
import requests

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

