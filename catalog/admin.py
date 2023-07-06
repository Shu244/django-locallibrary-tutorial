'''
This file defines the admin page that can be visited at domain:port/admin.
The admin page is useful to add, delete, or modify data defined in your ./models.py file
'''


from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


# One way to register models defined in ./models.py.
# In order to register a model, you need to provide the model and the rendering template.
# This is sufficient for simple models like Genre and Language, which only has a string field.
# By default, this way uses admin.ModelAdmin
admin.site.register(Genre)
admin.site.register(Language)


# This class crates a type of inline model, which is used by another model (i.e AuthorAdmin)
class BooksInline(admin.TabularInline):
    model = Book


# This class crates a type of inline model, which is used by another model (i.e BookAdmin)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


# Registers AuthorAdmin with Author model
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # Fields you see when you are viewing an author record. These strings are columns in the Author model/db table.
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # Fields you see when you are creating a new record or modifying a record
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # Inlines allows you to register another model under Author
    inlines = [BooksInline]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Manually register the BookAdmin with Book model
admin.site.register(Book, BookAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    # When you visit host:port/admin/catalog/bookinstance/, you get a navigation pane on the right
    # where you can filter based on these db columns. Note that "status" is a dropdown choice
    # and "due_back" is a date, both of which have default filter options.
    list_filter = ('status', 'due_back')

    # This organizes a group of fields; the first one has None heading and fields book, imprint, id.
    # The second one has "Availability" heading and fields status, due_back, and borrower.
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
