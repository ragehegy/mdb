from django.shortcuts import (render, redirect)
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.core.exceptions import (
    PermissionDenied
)
from django.urls import reverse
from core.forms import VoteForm, MovieImageForm
from core.models import Movie, Person, Vote

class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    # check for current movie object (in the MovieDetail view) for votes and user auth
    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied("Cannot change other user's vote!")
        return vote
    
    # Determine the URL to redirect to when the form is successfully validated.
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})
    
    def render_to_response(self):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    # pre populate the form with specific values for each specified fields in initial object
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial
    
    # Determine the URL to redirect to when the form is successfully validated.
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})

    # called by CreateView to return a response with the render template to the client.
    # here it's going to return a direct() to the MovieDetail view
    def render_to_response(self):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

class MovieList(ListView):
    model = Movie
    paginate_by = 10

class MovieDetail(DetailView):
    # model = Movie
    queryset = (Movie.objects.all_with_related_persons_and_scores())
    
    # overriding this method most often to add things to display in templates.
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_form'] = self.movie_image_form()
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(movie=self.object, user=self.request.user)
            if vote.id:
                vote_form_url = reverse(
                    'core:UpdateVote', kwargs={
                        'movie_id': vote.movie.id,
                        'pk': vote.id
                })
            else:
                vote_form_url = reverse(
                    'core:CreateVote', kwargs={
                        'movie_id': self.object.id
                })
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        return ctx

    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None

class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()

class MovieImageUpload(LoginRequiredMixin, CreateView):
    form_class = MovieImageForm
    
    # pre populate the form with specific values for each specified fields in initial object
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial
    
    # Determine the URL to redirect to when the form is successfully validated.
    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse("core:MovieDetail", kwargs={"pk": movie_id})
        return movie_detail_url

    # called by CreateView to return a response with the render template to the client.
    # here it's going to return a direct() to the MovieDetail view
    def render_to_response(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)
