from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from user.form import SignUpForm
from user.models import UserInfo

def home_page(request):
    return render(request, "base.html", {})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("valid")
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            mnumber = form.cleaned_data.get('mobile_no')
            print(mnumber)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            UserInfo(user_id=user.id, email=username, mobile_no=mnumber).save()
            return redirect('post_list')
    else:
        if request.user.is_authenticated:
            return redirect('post_list')
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
