from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("catalogo/", views.catalogo, name="catalogo"),
    path("jogo/<int:game_id>/", views.jogo_detalhe, name="jogo"),
    path("login/", views.login_view, name="login"),
    path("cadastro/", views.cadastro_view, name="cadastro"),
    path("perfil/", views.perfil_view, name="perfil"),
    path("perfil/editar-avatar/", views.editar_perfil, name="editar_perfil"),
    path("logout/", views.logout_view, name="logout"),
    path("admin/jogos/", views.admin_lista, name="admin_lista"),
    path("admin/jogos/novo/", views.admin_novo, name="admin_novo"),
    path("admin/jogos/<int:game_id>/editar/", views.admin_editar, name="admin_editar"),
    path("admin/jogos/<int:game_id>/deletar/", views.admin_deletar, name="admin_deletar"),
]