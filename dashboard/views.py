from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm


@login_required
def frontpage(request):
    return render(request, 'dashboard/frontpage.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
    
    return render(request, 'dashboard/signup.html', {'form': form})


def drawflow(request):
    nodos = ['Facebook', 'Github', 'Twitter']
    return render(request, 'dashboard/drawflow.html', {'nodos': nodos})


