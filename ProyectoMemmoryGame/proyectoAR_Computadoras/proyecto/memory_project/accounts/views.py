import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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

        user_exists = User.objects.filter(username=username).exists()
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("select_level")
        else:
            if user_exists:
                # Verificamos si existe pero está inactivo
                u = User.objects.get(username=username)
                if not u.is_active and u.check_password(password):
                    messages.error(request, "Tu cuenta no ha sido verificada. Revisa tu correo electrónico para activarla.")
                else:
                    messages.error(request, "Contraseña incorrecta.")
            else:
                messages.error(request, "Usuario no existe.")

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
            user = form.save(commit=False)
            user.is_active = False # Inactivo hasta verificar correo
            user.save()

            # 🔥 Generar código OTP de 4 dígitos
            otp = str(random.randint(1000, 9999))
            request.session['verification_otp'] = otp
            request.session['verification_userid'] = user.id

            # Enviar el correo
            try:
                send_mail(
                    subject="🚀 Código de Verificación para Memory Game",
                    message=f"¡Hola {user.username}!\n\nTu código de verificación es: {otp}\n\nIngrésalo en la página para activar tu cuenta y poder jugar.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.info(request, "Te hemos enviado un código de 4 dígitos a tu correo electrónico para verificar tu cuenta.")
            except Exception as e:
                # Si falla por configuración, mostramos un aviso y el código para no bloquear al usuario (solo por debug)
                print(f"Error al enviar correo: {e}")
                messages.warning(request, f"Ocurrió un error al enviar el correo al usuario. Por favor verifica las credenciales SMTP en settings.py")

            return redirect("verify_email")
        else:
            messages.error(request, "Error al crear la cuenta. Verifica los datos.")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


# =========================
# VERIFY EMAIL
# =========================
def verify_email(request):
    if request.user.is_authenticated:
        return redirect("select_level")

    # Necesitamos saber si hay un proceso de verificación pendiente en sesión
    user_id = request.session.get('verification_userid')
    otp_guardado = request.session.get('verification_otp')

    if not user_id or not otp_guardado:
        messages.error(request, "No hay ninguna verificación pendiente. Por favor, regístrate.")
        return redirect("register")

    if request.method == "POST":
        otp_ingresado = request.POST.get("otp", "").strip()

        if otp_ingresado == otp_guardado:
            # ¡Código Correcto!
            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()
                
                # Iniciar sesión automáticamente
                login(request, user)
                
                # Limpiar sesión
                del request.session['verification_otp']
                del request.session['verification_userid']

                messages.success(request, "¡Tu correo ha sido verificado! Bienvenido al juego.")
                return redirect("select_level")
            except User.DoesNotExist:
                messages.error(request, "Ocurrió un error. El usuario no fue encontrado.")
                return redirect("register")
        else:
            messages.error(request, "Código incorrecto. Inténtalo de nuevo.")

    return render(request, "accounts/verify.html")


# =========================
# LOGOUT
# =========================
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")