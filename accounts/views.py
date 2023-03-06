from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
#registration
def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")

    else:
         if request.method == "POST":
            form = RegistrationForm(request.POST or None)
        #check if form is valid
            if form.is_valid():
                User = form.save()

            #get the raw password
                raw_password = form.cleaned_data.get('password1')

            #authenticate the user
                User = authenticate(username=User.username, password=raw_password)

            #login the user
                login(request, User)

                return redirect("main:home")

         else:
            form = RegistrationForm()
         return render(request, "accounts/register.html", {"form": form})
               

#Login
def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:    
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            print(username, password)

        #check the credential
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("main:home")
                else:
                    return render(request, 'accounts/login.html', {"error": "your account has been disable."})
            else:
                return render(request, 'accounts/login.html',{"error":"invalis username or password"})
        return render(request, 'accounts/login.html')

#logout
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        print("logged out succesfully")
        return redirect("accounts:login")    
    else:
        return redirect("accounts:login")                            

