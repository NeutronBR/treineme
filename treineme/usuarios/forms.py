from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="E-mail")

    def cleaned_email(self):
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
