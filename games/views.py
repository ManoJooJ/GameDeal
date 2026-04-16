import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from . import mock_data
from .forms import LoginForm, CadastroForm, AvatarForm, GameForm


def _save_upload(file):
    path = os.path.join(settings.MEDIA_ROOT, file.name)
    with open(path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)
    return file.name


def home(request):
    return render(request, "games/home.html", {"destaques": mock_data.get_destaques()})


def catalogo(request):
    query = request.GET.get("q", "")
    games = mock_data.get_all()
    if query:
        games = [g for g in games if query.lower() in g["nome"].lower()]
    return render(request, "games/catalogo.html", {"games": games, "query": query})


def jogo_detalhe(request, game_id):
    game = mock_data.get_by_id(game_id)
    if not game:
        return redirect("catalogo")
    menor = min((v for v in game["precos"].values() if v), default=None)
    return render(request, "games/jogo.html", {"game": game, "menor": menor})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = mock_data.get_user(username)
        if user and user["password"] == password:
            request.session["user"] = username
            request.session["is_admin"] = user.get("is_admin", False)
            return redirect("perfil")
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "games/login.html", {"form": form})


def cadastro_view(request):
    form = CadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        if mock_data.user_exists(username):
            messages.error(request, "Usuário já existe.")
        else:
            mock_data.create_user(
                username,
                form.cleaned_data["email"],
                form.cleaned_data["password"],
            )
            request.session["user"] = username
            messages.success(request, f"Bem-vindo, {username}!")
            return redirect("perfil")
    return render(request, "games/cadastro.html", {"form": form})


def perfil_view(request):
    username = request.session.get("user")
    if not username:
        return redirect("login")
    user_data = mock_data.get_user(username) or {}
    avatar_form = AvatarForm()
    return render(request, "games/perfil.html", {
        "username": username,
        "user": user_data,
        "avatar_form": avatar_form,
        "jogos_destaque": mock_data.get_destaques(),
    })


def editar_perfil(request):
    username = request.session.get("user")
    if not username:
        return redirect("login")
    if request.method == "POST":
        arquivo = request.FILES.get("avatar")
        if arquivo:

            ext = os.path.splitext(arquivo.name)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
                messages.error(request, "Formato inválido. Use JPG, PNG ou WebP.")
                return redirect("perfil")
            
            nome_arquivo = f"avatar_{username}{ext}"
            caminho = os.path.join(settings.MEDIA_ROOT, nome_arquivo)
            with open(caminho, "wb+") as f:
                for chunk in arquivo.chunks():
                    f.write(chunk)
            
            mock_data.update_user(username, {"avatar": nome_arquivo})
            messages.success(request, "Foto de perfil atualizada!")
        else:
            messages.error(request, "Nenhum arquivo enviado.")
    return redirect("perfil")


def logout_view(request):
    request.session.flush()
    return redirect("home")


def admin_lista(request):
    return render(request, "games/admin_lista.html", {"games": mock_data.get_all()})


def admin_novo(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            imagem_nome = _save_upload(request.FILES["imagem"]) if request.FILES.get("imagem") else ""
            mock_data.create({
                "nome": cd["nome"], "genero": cd["genero"], "descricao": cd["descricao"],
                "imagem": imagem_nome if imagem_nome else "", "destaque": cd.get("destaque", False),
                "score": 0.0, "ano": 2026, "plat": "PC",
                "precos": {
                    "steam":  float(cd["preco_steam"])  if cd["preco_steam"]  else None,
                    "nuuvem": float(cd["preco_nuuvem"]) if cd["preco_nuuvem"] else None,
                    "epic":   float(cd["preco_epic"])   if cd["preco_epic"]   else None,
                }
            })
            messages.success(request, "Jogo adicionado!")
            return redirect("admin_lista")
    else:
        form = GameForm()
    return render(request, "games/admin_form.html", {"form": form, "titulo": "Novo Jogo"})


def admin_editar(request, game_id):
    game = mock_data.get_by_id(game_id)
    if not game:
        return redirect("admin_lista")
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            imagem_nome = _save_upload(request.FILES["imagem"]) if request.FILES.get("imagem") else game["imagem"]
            mock_data.update(game_id, {
                "nome": cd["nome"], "genero": cd["genero"], "descricao": cd["descricao"],
                "imagem": imagem_nome, "destaque": cd.get("destaque", False),
                "precos": {
                    "steam":  float(cd["preco_steam"])  if cd["preco_steam"]  else None,
                    "nuuvem": float(cd["preco_nuuvem"]) if cd["preco_nuuvem"] else None,
                    "epic":   float(cd["preco_epic"])   if cd["preco_epic"]   else None,
                }
            })
            messages.success(request, "Jogo atualizado!")
            return redirect("admin_lista")
    else:
        form = GameForm(initial={
            "nome": game["nome"], "genero": game["genero"], "descricao": game["descricao"],
            "preco_steam":  game["precos"].get("steam"),
            "preco_nuuvem": game["precos"].get("nuuvem"),
            "preco_epic":   game["precos"].get("epic"),
            "destaque": game.get("destaque", False),
        })
    return render(request, "games/admin_form.html", {"form": form, "titulo": "Editar Jogo", "game": game})


def admin_deletar(request, game_id):
    game = mock_data.get_by_id(game_id)
    if not game:
        return redirect("admin_lista")
    if request.method == "POST":
        mock_data.delete(game_id)
        messages.success(request, "Jogo removido.")
        return redirect("admin_lista")
    return render(request, "games/admin_deletar.html", {"game": game})