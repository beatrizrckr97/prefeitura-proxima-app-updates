# solicitacoes/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("Página inicial das solicitações.")

