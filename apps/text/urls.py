"""
URLconf for the text application. It defines urls for creating, listing, and
editing text objects.

A comprehensive explanation of the regex ^(?P<id>\d+)/$ follows:

  ^                     = Start of the line.
  (?P<[label]>[regex])  = Tell Django to put everything captured by [regex]
                          into a variable called [label].
  \d+                   = One or more digits.
  $                     = End of the line.

  So putting this together:

  ^(?P<id>\d+)/$ captures a URL of the form /[id]/ where [id] is one or more
  digits, and then stores the [id] in a variable called id and sends it to the
  view as a **kwarg.

"""
from text.models import Document
from django.conf.urls.defaults import *
from text.views import list_view, document_view, edit_view, submit
from django.views.generic.create_update import create_object

urlpatterns = patterns('',

                        # Browse a list of all the files.
                        url(r'^browse/$',
                            list_view,
                            name='text_browse'),

                        # Upload text of your own.
                        url(r'^$',
                            create_object,
                            {'model': Document,
                            'template_name':'index.html'},
                            name='text_home'),

                        # Upload text of your own.
                        url(r'^upload/$',
                            create_object,
                            {'model': Document},
                            name='text_upload'),

                        # View a single document.
                        url(r'^(?P<id>\d+)/$',
                            document_view,
                            name='text_document'),

                        # Edit a single document.
                        url(r'^edit/(?P<id>\d+)/$',
                            edit_view,
                            name='text_edit'),

                        # Submit forms.
                        url(r'^submit/$',
                            submit,
                            name='text_create'),

                        # Update existing.
                        url(r'^submit/(?P<id>\d+)/$',
                            submit,
                            name='text_update'),
)
