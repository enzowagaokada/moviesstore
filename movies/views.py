from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MoviePetition
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
   # Exclude movies hidden by the current user
    if request.user.is_authenticated:
        movies = Movie.objects.exclude(hidden_by=request.user)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)
@login_required
def hide_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.hidden_by.add(request.user)
    return redirect('movies.show', id=id)

@login_required
def unhide_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.hidden_by.remove(request.user)
    return redirect('movies.show', id=id)

@login_required
def hidden_movies(request):
    template_data = {}
    template_data['title'] = 'Hidden Movies'
    template_data['movies'] = Movie.objects.filter(hidden_by=request.user)
    return render(request, 'movies/hidden.html', {'template_data': template_data})

@login_required
def petition_list(request):
    petitions = MoviePetition.objects.all()
    return render(request, 'movies/petition_list.html', {'petitions': petitions})

@login_required
def create_petition(request):
    if request.method == 'POST':
        movie_title = request.POST.get('movie_title')
        description = request.POST.get('description')
        petition = MoviePetition.objects.create(
            movie_title=movie_title,
            description=description,
            created_by=request.user
        )
        petition.votes.add(request.user)
        return redirect('movies.petition_list')
    return render(request, 'movies/create_petition.html')

@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(MoviePetition, id=petition_id)

    if request.user in petition.votes.all():
        petition.votes.remove(request.user)
    else:
        petition.votes.add(request.user)

    return redirect('movies.petition_list')