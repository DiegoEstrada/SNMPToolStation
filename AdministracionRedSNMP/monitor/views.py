from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'adminlte/index.html')

def verAgentes(request):
    return render(request, 'adminlte/agentes.html')

def agregarAgente(request):
    return render(request, 'adminlte/agregarAgente.html')

def verAgente(request):
    return render(request, 'adminlte/verAgente.html')

def estadoAgente(request):
    return render(request, 'adminlte/verAgente.html')