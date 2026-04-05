from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.user.is_authenticated:
        return redirect("select_level")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("select_level")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "accounts/login.html")


# =========================
# REGISTER
# =========================
def register_view(request):
    if request.user.is_authenticated:
        return redirect("select_level")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # 🔥 Login automático después de registrarse
            login(request, user)

            messages.success(request, "Cuenta creada correctamente.")
            return redirect("select_level")
        else:
            messages.error(request, "Error al crear la cuenta. Verifica los datos.")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


# =========================
# LOGOUT
# =========================
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")