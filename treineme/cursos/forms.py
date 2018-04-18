from django import forms


class ContatoCurso(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    mensagem = forms.CharField(label='Digite sua mensagem', widget=forms.Textarea(attrs={'class': 'form-control'}))
