from django.shortcuts import redirect

ROTAS_PROTEGIDAS = [
    '/perfil/',
    '/admin/jogos/',
]


class SessaoAuthMiddleware:
    """
    Middleware customizado que protege rotas autenticadas via sessão.
    Se não houver 'user' na sessão, redireciona para /login/.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for rota in ROTAS_PROTEGIDAS:
            if request.path.startswith(rota):
                if not request.session.get('user'):
                    return redirect(f'/login/?next={request.path}')
                break
        return self.get_response(request)