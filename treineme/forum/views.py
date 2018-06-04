from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView
# Create your views here.

from forum.models import Topico

# class ForumView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'forum.html')
#
# class ForumView(TemplateView):
#    template_name = 'forum.html'


class ForumView(ListView):
    model = Topico
    paginacao = 10
    template_name = 'forum.html'
