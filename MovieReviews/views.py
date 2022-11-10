from django.shortcuts import render, redirect
import json
import requests

API_KEY = '444422-MovieRev-XMHI8X3L'
def index(request):

    search = 'love'
    if request.method == 'POST':
        search = request.POST.get('search')

    response = requests.get('https://tastedive.com/api/similar?q=' + search + '&type=movies&info=1&limit=20&k=' + API_KEY)
    data = response.json()
    movies = data['Similar']['Info']
    movies.extend(data['Similar']['Results'])

   # for movie in movies:
      #  responseImages = requests.get('https://serpapi.com/playground?q=titanicmovie&tbm=isch&ijn=0')
      #  imageSearch = responseImages.json()
       # movie['wUrl'] = imageSearch['images_results']['thumbnail']

    context = {'movies': movies}
    return render(request, 'review/index.html', context)

