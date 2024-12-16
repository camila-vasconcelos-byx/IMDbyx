from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'IMDbyx/index.html')

def movie_detail(request, movie):
    return render(request, 'IMDbyx/movie.html')
