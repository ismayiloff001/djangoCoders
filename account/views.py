from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from services.generator import Generator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
User = get_user_model()

def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)

            login(request, user)
            return redirect('/')
        else:
            print(form.errors)
    context = {
        "form":form
    }
    return render(request, "account/login.html", context)

def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            new_user.set_password(password)
            new_user.is_active = False
            new_user.activation_code = Generator.create_code_for_activate(size=6,model_=User)
            new_user.activation_code_expires_at = timezone.now() + timezone.timedelta(minutes=15)
            new_user.save()


            #send mail
            send_mail(
                "Activation Code",
                f"Sizin aktivasiya kodunuz {new_user.activation_code}",

                settings.EMAIL_HOST_USER,
                [new_user.email]
            )

            # login(request, new_user)

            return redirect('activate-account', slug = new_user.slug)
        
        else:
            print(form.errors)
    context= {
        "form": form

    }

    return render(request, "account/register.html", context)

def logout_view(request):
    logout(request)
    
    return redirect('/list')

# @check_activation_code_time
def activate_account_view(request, slug):
    user  = get_object_or_404(User, slug=slug)
    context = {}

    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.activation_code:
            user.is_active = True
            user.activation_code = None
            user.activation_code_expires_at = None
            user.save()

            login(request, user)
            return redirect('/login/')
        else:
            return "Yalnis sifre!"
    return render(request, 'account/activate.html', context)