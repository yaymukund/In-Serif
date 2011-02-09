from django.template import RequestContext
from text.models import Document, DocumentForm

from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object, update_object

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login

def create_view(request):
  """Generate a view to create new documents."""
  return create_object(request, Document)

@login_required
def list_view(request):
  """Generate a view to list documents."""
  queryset = Document.objects.filter(user=request.user)
  return object_list(request, queryset, template_object_name='document')

def document_view(request, id):
  """Generate a view to display a single document.
  
  Keyword arguments:
  id -- The unique primary key id of the document.
  
  """
  id = int(id)
  document = Document.objects.get(id=id)
  
  # If the user isn't logged in, make them log in.
  if document.private and not request.user.is_active:
    return redirect_to_login(request.path)

  # If the user is logged in and they don't own the document, reject!
  if document.private and request.user != document.user:
    return direct_to_template(request, template='404.html')
  
  return direct_to_template(request, template='text/document_detail.html', \
      extra_context={'document': document})

@login_required
def edit_view(request, id):
  """Edit an existing document.

  Keyword arguments:
  id -- The unique primary key id of the document.

  """
  id = int(id)
  document = Document.objects.get(id=id)
  if request.user == document.user:
    return update_object(request, Document, id, template_object_name='document')
  else:
    return direct_to_template(request, template='404.html')

def submit(request, id=None):
  """Create a new document or update an existing document.

  Keyword arguments:
  id -- If we are updating an existing document, this is its id. Otherwise, None.
  
  """
  # Create a new document if we have to.
  if id is None:
    if not request.user.is_active:
      document = Document()
    else:
      document = Document(user=request.user)

  # Otherwise, we get the existing document to update.
  else:
    try:
      document = Document.objects.get(id=id, user=request.user)
    except:
      return direct_to_template(request, template='404.html')

  # Fill the remaining values and save.
  form = DocumentForm(request.POST, instance=document)
  if form.is_valid():
    form.save()

  return HttpResponseRedirect(document.get_absolute_url())
