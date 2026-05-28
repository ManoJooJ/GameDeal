from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    nome = models.CharField(max_length=200)
    genero = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    score = models.FloatField(default=0.0)
    ano = models.IntegerField(default=2024)
    plat = models.CharField(max_length=100, default='PC')
    imagem = models.CharField(max_length=500, blank=True)
    destaque = models.BooleanField(default=False)
    preco_steam = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    preco_nuuvem = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    preco_epic = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-destaque', 'nome']
        verbose_name = 'Jogo'
        verbose_name_plural = 'Jogos'

    def __str__(self):
        return self.nome

    def menor_preco(self):
        precos = [p for p in [self.preco_steam, self.preco_nuuvem, self.preco_epic] if p is not None]
        return min(precos) if precos else None


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'Perfil de {self.user.username}'