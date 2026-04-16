from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=50)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

class CadastroForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=50)
    email    = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput, min_length=6)
    confirm  = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("confirm"):
            raise forms.ValidationError("As senhas não conferem.")
        return cleaned

class AvatarForm(forms.Form):
    avatar = forms.ImageField(label="Nova foto de perfil")

class GameForm(forms.Form):
    nome        = forms.CharField(label="Nome do Jogo", max_length=100)
    genero      = forms.CharField(label="Gênero", max_length=50)
    descricao   = forms.CharField(label="Descrição", widget=forms.Textarea(attrs={"rows": 3}))
    preco_steam = forms.DecimalField(label="Preço Steam (R$)", min_value=0, required=False)
    preco_nuuvem= forms.DecimalField(label="Preço Nuuvem (R$)", min_value=0, required=False)
    preco_epic  = forms.DecimalField(label="Preço Epic (R$)", min_value=0, required=False)
    destaque    = forms.BooleanField(label="Destaque na Home?", required=False)
    imagem      = forms.ImageField(label="Imagem do Jogo", required=False)