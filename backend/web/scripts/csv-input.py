# python manage.py runscript csv-input --script-args 20m
from sys import stderr, stdout
from handler.models import Movies, Genre, Links
import csv

# Function that loads in items from Movies and Links csv files:
# The same process can be completed again by replicating this step
def run(*args):
    # data paths for movies we excpect the command to recieve:
    if '1m' in args:
        path = '/data/ml-latest-small/movies.csv'
        links_path = '/data/ml-latest-small/links.csv'
    
    if '25m' in args:
            path = '/data/ml-25m/movies.csv'
            links_path = '/data/ml-25m/links.csv'
    else:
        path = '/data/ml-latest-small/movies.csv'
        links_path = '/data/ml-latest-small/links.csv'
    # Add Movies
    with open(path) as f:
        reader = csv.reader(f)
        next(reader, None)
        i = 0
        for row in reader:
            # This must match target Model:
            moviecreated = Movies.objects.get_or_create(
                movieId = row[0],
                title = row[1]
            ),

            # Feedback on process
            i += 1
            if i % 1000 == 0:
                stdout.write(f'!! added {row[1]} {i}th Movies \n')

    # Add Genres
    with open(path) as f:
        reader = csv.reader(f)
        next(reader, None)
        i = 0 
        for row in reader:
            l = row[2].split('|')
            for g in l:
                # Again this must match target Model
                movie = Movies.objects.get(movieId=row[0])
                genrecreated = Genre.objects.get_or_create(
                    name = g
                    )
                # Many - Many relationship
                genre = Genre.objects.get(name=g)
                genre.movies.add(movie)

                # Feedback in process
                i += 1
                if i % 1000 == 0:
                    stdout.write(f'!! Linked {row[1]} to {g}. - {i}th link \n')

    # Add Links    
    # data paths for links we excpect the command to recieve:
    
    with open(links_path) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            try:
                _, created = Links.objects.get_or_create(
                        movie = Movies.objects.get(movieId=row[0]),
                        movieId = row[0],
                        imdbId = row[1],
                        tmdbId = row[2],
                )
            except:
                stdout.write(f'!! Movie: {row[0]}, failed to create Link\n')


