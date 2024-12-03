from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})
