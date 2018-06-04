from django.urls import path
from forum.views import ForumView

# app_name = namespace
app_name = 'forum'
urlpatterns = [
    path('<slug:atalho_curso>', ForumView.as_view(), name='home'),

]
