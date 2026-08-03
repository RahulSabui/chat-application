from django.urls import path

from .views.conversation_view import CreatePrivateConversationView

urlpatterns = [
    path(
        "conversation/private/",
        CreatePrivateConversationView.as_view(),
    ),
]