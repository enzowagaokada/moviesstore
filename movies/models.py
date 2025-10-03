from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    hidden_by = models.ManyToManyField(User, related_name='hidden_movies', blank=True)

    def __str__(self):
        return str(self.id) + " - " + self.name

    def is_hidden_by_user(self, user):
        return self.hidden_by.filter(id=user.id).exists()

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
class MoviePetition(models.Model):
    movie_title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, related_name='voted_petitions', blank=True)
    
    def total_votes(self):
        return self.votes.count()
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.movie_title