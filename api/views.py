from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
import json

@login_required
def autocomplete(request):
    raise Http404
    return HttpResponse(json.dumps({}))
