from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.
def home(request):
    query = request.GET.get("title")
    allMovies = None
    if query:
        allMovies = Movie.objects.filter(name__icontains=query)
    else:    
        allMovies = Movie.objects.all()
        print('allMovies')

    context = {
        "movies":allMovies,
    }

    return render(request, 'main/index.html', context)

#detail page
def detail(request, id):
    movie = Movie.objects.get(id=id)  #select * from where id-id
    reviews = Review.objects.filter(movie=id).order_by("-comment")
    context={
        "movie":movie,
        "reviews":reviews
    }

    return render(request, 'main/details.html', context)


#add movie to the database

def add_movies(request):
    if request.method == "POST":
        form = MovieForm(request.POST or None)

        #check if form is valid
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:home")

    else:
         form = MovieForm()
    return render(request, 'main/addmovies.html', {"form":form})    

def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("main:detail", id)

        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {"form": form})
    else:
        return redirect("accounts:login")

