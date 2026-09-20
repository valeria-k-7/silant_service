from django.urls import path

from .views import home, reference_index


app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('references/', reference_index, name='references'),
]
