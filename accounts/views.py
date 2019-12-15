from django.shortcuts import render ,redirect
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
# Create your views here.

from accounts.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


class ProfileView(TemplateView):
    template_name = 'myprofile.html'