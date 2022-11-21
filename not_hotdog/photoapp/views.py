# allows us to retrieve an object from the database, 
# preventing a DoesNotExists error and raising a HTTP 404 exception
from django.shortcuts import get_object_or_404
# aise an HTTP 403 exception when called
from django.core.exceptions import PermissionDenied
# for building CRUD functionality
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
# to assert the users have the right permissions when accessing to a view
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# used in CBVs to redirect the users to a specific URL
from django.urls import reverse_lazy
# to retrieve and update database rows (photo objects)
from .models import Photo


# Create your views here.
class PhotoListView(ListView):
    model = Photo
    template_name = 'photoapp/list.html'
    context_object_name = 'photos'

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photoapp/detail.html'
    context_object_name = 'photo'


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    # create a form with these fields
    fields = ['title', 'description', 'image']
    template_name = 'photoapp/create.html'
    # Users will be redirected to the photo dashboard 
    # if the photo creation was successful
    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        # setting up the user that’s making the request 
        # as the submitter of the photo form
        form.instance.submitter = self.request.user
        return super().form_valid(form)


# checks if the user that’s trying to update or delete a photo 
# actually submitted it
class UserIsSubmitter(UserPassesTestMixin):
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'photoapp/update.html'
    model = Photo
    # defines the fields the user will be able to edit
    fields = ['title', 'description']
    success_url = reverse_lazy('photo:list')


class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'photoapp/delete.html'
    model = Photo
    success_url = reverse_lazy('photo:list')


class PhotoMyListView(ListView):
    model = Photo
    template_name = 'photoapp/mylist.html'
    context_object_name = 'myphotos'