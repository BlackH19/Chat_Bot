from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("/ask", views.chat, name="ask_question")
]