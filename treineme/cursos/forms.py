from django import forms
# from django.core.mail import send_mail
from django.conf import settings
from mail import envia_email_template
from cursos.models import Comentario, Alternativa


class ContatoCurso(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    mensagem = forms.CharField(label='Digite sua mensagem', widget=forms.Textarea(attrs={'class': 'form-control'}))

    def envia_email(self, curso):
        assunto = ('{} contato'.format(curso))
        # pdb.set_trace()
        # mensagem = 'Nome: {}; E-mail: {}; Mensagem: {}'.format(
        #     self.cleaned_data['nome'],
        #     self.cleaned_data['email'],
        #     self.cleaned_data['mensagem'],
        # )
        # send_mail(assunto, mensagem, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])

        template_name = 'email_contato.html'
        contexto = {
            'nome': self.cleaned_data['nome'],
            'email': self.cleaned_data['email'],
            'mensagem': self.cleaned_data['mensagem'],
        }
        envia_email_template(assunto, template_name, contexto, [settings.CONTACT_EMAIL])


class ComentarioForm(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ['comentario']


# class RespostaForm(forms.Form):
#     alternativas = forms.ModelChoiceField(queryset=Alternativa.objects.all(), widget=forms.RadioSelect)
