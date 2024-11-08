from django.shortcuts import redirect
from django.urls import reverse

class TwoFactorAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.tiene_2fa_configurado() and not request.session.get('verificado_2fa', False):
                if request.path not in [reverse('auth:verificar_2fa'), reverse('auth:logout')]:
                    return redirect('auth:verificar_2fa')
        response = self.get_response(request)
        return response