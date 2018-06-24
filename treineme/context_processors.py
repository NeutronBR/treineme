from django.conf import settings
# from django.contrib.sites.shortcuts import get_current_site


# https://stackoverflow.com/a/433209/6186117
# Make a context_processors.py file in your app directory. Let's say I want to have the ADMIN_PREFIX_VALUE value in every context:
# from django.conf import settings # import the settings file
#
# def admin_media(request):
#     # return the value you want as a dictionnary. you may add multiple values in there.
#     return {'ADMIN_MEDIA_URL': settings.ADMIN_MEDIA_PREFIX}
# add your context processor to your settings.py file:
# TEMPLATES = [{
#     # whatever comes before
#     'OPTIONS': {
#         'context_processors': [
#             # whatever comes before
#             "your_app.context_processors.admin_media",
#         ],
#     }
# }]
# Use RequestContext in your view to add your context processors in your template. The render shortcut does this automatically:
# from django.shortcuts import render
#
# def my_view(request):
#     return render(request, "index.html")
# and finally, in your template:
# ...
# <a href="{{ ADMIN_MEDIA_URL }}">path to admin media</a>
# ...


def nome_empresa(request):
    return {'NOME_EMPRESA': settings.NOME_EMPRESA}


def treineme_site(request):
    return {'TREINEME_SITE': settings.TREINEME_SITE}
    # return {'TREINEME_SITE': get_current_site()}
