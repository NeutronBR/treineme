from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from usuarios.models import SenhaReset
from usuarios.utils import gerar_hash_chave
from mail import envia_email_template


Usuario = get_user_model()

# import pdb


class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="E-mail")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está sendo usado')
        else:
            return email

    def salvar(self, commit=True):
        usuario = super(RegistroForm, self).save(commit=False)
        usuario.email = self.cleaned_data['email']
        if commit:
            usuario.save()
        return usuario


class EditarUsuarioForm(forms.ModelForm):
    # é chamado pelo if is_valid() na view
    def clean_email(self):
        # pdb.set_trace()
        email = self.cleaned_data['email']

        # instance é uma variável do ModelForm, que é a instância sendo "trabalhada" no momento
        # garantir que o email digitado não exista no banco, mas não comparando consigo próprio (para o caso de edição sem alteração do email)
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Este e-mail já está sendo usado')
        else:
            return email

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ResetSenhaForm(forms.Form):

    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        else:
            raise forms.ValidationError('Nenhum usuário encontrado com o e-mail informado')

    def save(self):
        usuario = Usuario.objects.get(email=self.cleaned_data['email'])
        chave = gerar_hash_chave(usuario.username)
        reset = SenhaReset(usuario=usuario, chave=chave)
        reset.save()
        template_name = 'reset_senha_email.html'
        # assunto = 'Recuperação de senha no Treine-me {}'.format()
        assunto = 'Recuperação de senha no Treine-me'
        contexto = {
            'reset': reset,
            'nome': usuario.get_full_name(),
        }
        envia_email_template(assunto, template_name, contexto, [usuario.email])
