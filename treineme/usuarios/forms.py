from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

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
