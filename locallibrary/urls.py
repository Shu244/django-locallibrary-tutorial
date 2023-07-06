'''
URLs for the project locallibrary.
'''


from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += [
    # Imports urls from ../catalog/urls.py
    path('catalog/', include('catalog.urls')),
]


# Use static() to add url mapping to serve static files during development (only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Add URL maps to redirect the base URL to our application
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]


# Add Django site authentication urls (for login, logout, password management)
# The following urls are added
#     accounts/ login/ [name='login']
#     accounts/ logout/ [name='logout']
#     accounts/ password_change/ [name='password_change']
#     accounts/ password_change/done/ [name='password_change_done']
#     accounts/ password_reset/ [name='password_reset']
#     accounts/ password_reset/done/ [name='password_reset_done']
#     accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
#     accounts/ reset/done/ [name='password_reset_complete']
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
