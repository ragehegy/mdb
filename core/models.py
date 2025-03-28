from django.db import models
from django.db.models import Sum
from mdb import settings
from django.contrib.auth import get_user_model
from uuid import uuid4


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        qs = self.get_queryset()
        #select related works on joining 2 db tables before sending the query
        qs = qs.select_related('director') 

        #prefetch retrieve all required IDs in the query from Person model and joins it with Movie person fields(writers, actors) using python but not the db query (i.e. list/sets joins)
        qs = qs.prefetch_related('writers', 'actors')
        
        return qs

    def all_with_related_persons_and_scores(self):
        qs = self.all_with_related_persons()
        qs = qs.annotate(score=Sum('vote__value'))
        return qs

    def top_movies(self, limit=10):
        qs = self.get_queryset()
        qs = qs.annotate(vote_sum=Sum('vote__value'))
        qs = qs.exclude(vote_sum=None)
        qs = qs.order_by('-vote_sum')
        qs = qs[:limit]
        return qs

class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G,
         'G - General Audiences'),
        (RATED_PG,
         'PG - Parental Guidance '
         'Suggested'),
        (RATED_R, 'R - Restricted'),
    )
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(
        to="Person",
        on_delete=models.SET_NULL,
        related_name="directed",
        null=True,
        blank=True
    )
    writers = models.ManyToManyField(
        to="Person",
        # through="Role",
        related_name="writing_credits",
        blank=True
    )
    actors = models.ManyToManyField(
        to='Person',
        through='Role',
        related_name='acting_credits',
        blank=True
    )

    objects = MovieManager()

    class Meta:
        ordering = ('-year', 'title')

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

def movie_directory_path_with_uuid(instance, filename):
    return '{}/{}.{}'.format(
        instance.movie_id,
        uuid4(),
        filename.split('.')[-1]
    )

class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded=models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(
        "Movie",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
        

class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related('directed', 'writing_credits', 'roe_set__movie')

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)

    objects = PersonManager()

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        if self.died:
            return '{}, {} ({} - {})'.format(self.last_name, self.first_name, self.born, self.died)
        return '{}, {} ({})'.format(self.last_name, self.first_name, self.born)

class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{} {} {}'.format(self.movie_id, self.person_id, self.name)

    class Meta:
        unique_together = ("movie", "person", "name")

class VoteManager(models.Manager):
    def get_vote_or_unsaved_blank_vote(self, movie, user):
        try:
            return Vote.objects.get(
                movie=movie,
                user=user
            )
        except Vote.DoesNotExist:
            return Vote(
                movie=movie,
                user=user
                )

class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = {
        (UP, "UPVOTE"),
        (DOWN, "DOWNVOTE")
    }

    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user =  models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    movie =  models.ForeignKey(
        Movie,
        on_delete=models.CASCADE
    )
    voted_on = models.DateTimeField(
        auto_now=True
    )

    objects = VoteManager()

    class Meta:
        unique_together = ("user", "movie")