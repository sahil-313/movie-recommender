from . import views
from .models import Movie
from django.shortcuts import render

# HINT: Create a view to provide movie recommendations list for the HTML template
def movie_recommendation_view(request):
    if request.method == "GET":
        # The context/data to be presented in the HTML template
        context = {}
        # Render a HTML page with specified template and context
        return render(request, "movierecommender/movie_list.html", context)
    
def generate_movies_context():
    context = {}

    recommended_count = Movie.objects.filter(
        recommended = True
    ).count()

    if recommended_count == 0:
        movies = Movie.objects.filter(
            watched = False
        ).order_by("-vote_count")[:30]
    else:
        movies = Movie.objects.filter(
            watched = False
        ).filter(
            recommended = True
        ).order_by("-vote_count")[:30]

    context["movie_list"] = movies
    return context