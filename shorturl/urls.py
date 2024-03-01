from django.urls import path
from django.views.generic import TemplateView

from .views import index, redirct_url, detail, IndexAPIView


app_name = 'shorturl'
urlpatterns = [
    path('', index, name='index'),
    path('<str:code>/', redirct_url, name='redirct_url'),
    path("detail", detail, name="detail"),

    path('api/shorturl', IndexAPIView.as_view()),
]
