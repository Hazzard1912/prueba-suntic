from .forms import CustomUserCreationForm, LoginForm
from .forms import VerificacionTOTPForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from urllib.parse import unquote
import qrcode
import qrcode.image.svg
from urllib.parse import quote


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'auth/auth_form.html'
    success_url = reverse_lazy('documents:document_list')
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.tiene_2fa_configurado():
            return redirect('auth:verificar_2fa')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Iniciar Sesión',
            'button_text': 'Entrar',
            'link_text': '¿No tienes cuenta? Regístrate',
            'link_url': 'auth:registro'
        })
        return context
    

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/auth_form.html', {
        'form': form,
        'title': 'Registro',
        'button_text': 'Registrarse',
        'link_text': '¿Ya tienes cuenta? Inicia sesión',
        'link_url': 'auth:login'
    })

def generar_qr(request, qr_url):
    qr_url = unquote(qr_url)
    img = qrcode.make(qr_url, image_factory=qrcode.image.svg.SvgImage)
    response = HttpResponse(content_type='image/svg+xml')
    img.save(response)
    return response


@login_required
def configurar_2fa(request):
    device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()
    if not device:
        device = TOTPDevice.objects.create(
            user=request.user,
            name='default',
            confirmed=False
        )
    
    qr_url = quote(device.config_url, safe='')

    if request.method == 'POST':
        form = VerificacionTOTPForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            if device.verify_token(codigo):
                device.confirmed = True
                device.save()
                messages.success(request, 'Autenticación de dos factores activada correctamente.')
                return redirect('home')
            else:
                messages.error(request, 'Código incorrecto. Por favor, intenta nuevamente.')
    else:
        form = VerificacionTOTPForm()

    return render(request, 'auth/configurar_2fa.html', {
        'form': form,
        'qr_url': qr_url
    })


@login_required
def verificar_2fa(request):
    if not request.user.tiene_2fa_configurado():
        return redirect('configurar_2fa')

    if request.method == 'POST':
        form = VerificacionTOTPForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            device = TOTPDevice.objects.get(user=request.user, confirmed=True)
            
            if device.verify_token(codigo):
                request.session['verificado_2fa'] = True
                return redirect(request.session.get('next', 'documents:document_list'))
            else:
                messages.error(request, 'Código incorrecto. Por favor, intenta nuevamente.')
    else:
        form = VerificacionTOTPForm()

    return render(request, 'auth/verificar_2fa.html', {'form': form})


@login_required
def desactivar_2fa(request):
    if request.method == 'POST':
        request.user.desactivar_2fa()
        messages.success(request, 'La autenticación de dos factores ha sido desactivada.')
        return redirect('auth:seguridad')
    return render(request, 'auth/desactivar_2fa.html')


@login_required
def seguridad(request):
    return render(request, 'auth/seguridad.html')