'''
The views defined here are responsible for handling http request by querying models and templates.
'''

import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


def index(request):
    # Gathering data from models for index page
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Capturing session data stored in request object
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    # The context key-value arguments are unwrapped and passed to the template
    return render(
        request,
        'index.html',
        context={'num_books': num_books,
                 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors,
                 'num_visits': num_visits},
    )


# This class name does not matter.
# By default, the template used is ./templates/catalog/<model>_list.html.
# By default, the retrieved objects will be named <model>_list when passed to the template.
class BookListView(generic.ListView):
    model = Book
    # Show 10 models before starting pagination
    paginate_by = 10


# By default, the template used is ./templates/catalog/<model>_detail.html.
class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


# LoginRequiredMixin acts similarly to the decorator @login_required
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    # Defining new path for template
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    # Override this method to change the list of records returned
    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    # Behaves similar to decorator @permission_required
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# If the user is logged in, then your view code will execute as normal.
# If the user is not logged in, he will redirect to the login URL (defined in settings.LOGIN_URL).
# If the user succeeds in logging in then they will be returned back to this page.
@login_required
# Returns 403 (HTTP Status Forbidden) if logged in user does not have permissions
@permission_required('catalog.can_mark_returned', raise_exception=True)
# This function accepts pk argument because it is mapped to an url in ./urls.py that has pk url argument
def renew_book_librarian(request, pk):
    # Returns exception if unable to get object
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        # Creating the form we defined in ./forms.py.
        # Populate it with data from the request
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            # Save the book instance data to db
            book_instance.save()
            # reverse('all-borrowed') returns the appropriate url named all-borrowed
            # HttpResponseRedirect redirects to that url
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # Creating a new form with initial values
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    # Context key-values are unwrapped and passed to the template; in the template,
    # you can access form and book_instance.
    return render(request, 'catalog/book_renew_librarian.html', context)


# CreateView is a generic view is designed to create and save a new instance of a model.
# Uses the template <model>_form.html
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    # This specifies the fields to include in the form
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    # The initial values in the form
    initial = {'date_of_death': '11/06/2020'}
    permission_required = 'catalog.can_mark_returned'


# UpdateView is a generic view is designed to update a model.
# Uses the template <model>_form.html
class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    permission_required = 'catalog.can_mark_returned'


# Uses the template <model>_confirm_delete.html.
class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    # This is the URL that the user will be redirected to after a successful deletion.
    # reverse_lazy is a lazily executed version of reverse, meaning it's not called until it's needed.
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


# Classes created for the forms challenge
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'
