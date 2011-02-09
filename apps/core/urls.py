"""
URLconf for the core of the application, which draws from various URLconfs from
the registration and text app libraries.

"""

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                        # Delegate to the registration URLconf within the
                        # registration app.
                        (r'^', include('registration.urls')),

                        # Delegate to the text URLconf within the text app.
                        (r'^', include('text.urls')),

                        # Serve media files, ONLY FOR DEVELOPMENT.
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/mukund/Documents/projects/inserif/static/'}),

                        # Setup Django's admin site.
                        (r'^admin/', include(admin.site.urls)),
)
