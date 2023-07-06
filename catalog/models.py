'''
This is where you can create your models, which will be translated to database tables and columns.
Models are database agnostic, and Django automatically handles boilerplate database commands (in ./migrations/)
'''


# Generates a Universally Unique Identifier using pseudo randomness.
# Probability of a duplicate is so low, it is essentially unique.
import uuid

from django.db import models
from django.urls import reverse
from datetime import date
# User is an automatically created model in Django
from django.contrib.auth.models import User


# Creates a Genre table in the database
class Genre(models.Model):
    # Defines fields/cols in the table
    name = models.CharField(
        max_length=200,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"
        )

    # Useful to get string representation once you have a model instance
    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    # A Book model can contain many genres (and a genre can be included in many Book models)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        # When you query for Book models, the list will be returned sorted by these criteria
        ordering = ['title', 'author']

    # This function is used because Genre is a manyToMany relationship, so django does not allow genre
    # to be used as a field in admin.py due to db query costs.
    # This function defines what to display when genre is used as a field.
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    # This is the header when display_genre is used as a field.
    display_genre.short_description = 'Genre'

    # This is useful when you have an instance of this Model
    def get_absolute_url(self):
        # Uses the name of the URL defined in ./urls.py to generate the URL for this model. If self.id=1,
        # the generate URL is host:port/admin/catalog/book/1
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    # Note that User is a model automatically provided by Django!
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='d',
        help_text='Book availability')

    class Meta:
        ordering = ['due_back']
        # Adding custom permissions. These permissions must be granted to Users,
        # which you can do at host:port/admin/auth/user/1/change/.
        # As the user logs in, we can define logic conditioned on these permissions.
        # For example, we can condition what the user sees. This permission is used in ./views.py (renew_book_librarian)
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    # If verbose name is not provided, one is automatically created: i.e. first_name --> First Name
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)
