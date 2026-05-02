from django.core.management import BaseCommand
from ...models import Movie


# Check if genres are valid
def check_valid_genres(genres: str) -> bool:
    if bool(genres and not genres.isspace()) and genres != 'na':
        return True
    else:
        return False

# Add a Jaccard similarity method here
def jaccard_similarity(list1: list, list2: list) -> float:
    set1 = set(list1)
    set2 = set(list2)
    return float(len(set1.intersection(set2))/len(set1.union(set2)))

# Add a movie similarity method here
def similarity_between_movies(movie1: Movie, movie2: Movie) -> float:
    if check_valid_genres(movie1.genres) and check_valid_genres(movie2.genres):
        movie1_genres = movie1.genres.split()
        movie2_genres = movie2.genres.split()
        return jaccard_similarity(movie1_genres, movie2_genres)
    else:
        return 0

class Command(BaseCommand):
    help = 'Recommend movies'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        # Figure the recommended field for each unwatched movie
        # Based on the similarity on movie genres
        THRESHOLD = 0.8
        watched_movies = Movie.objects.filter(watched=True)
        unwatched_movies = Movie.objects.filter(watched=False)

        for unwatched_movie in unwatched_movies:
            max_similarity = 0
            will_recommend = False

            for watched_movie in watched_movies:
                similarity = similarity_between_movies(unwatched_movie, watched_movie)
                if similarity >= max_similarity:
                    max_similarity = similarity

                if max_similarity >= THRESHOLD:
                    break

            if max_similarity >= THRESHOLD:
                will_recommend = True
                print(f"Find a movie recommendation: {unwatched_movie.original_title}")

            unwatched_movie.recommended = will_recommend
            unwatched_movie.save()

# python manage.py make_recommendations