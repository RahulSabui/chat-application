from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.serializers.conversation_serializer import (
    ConversationSerializer,
)

from chat.services.conversation_service import (
    ConversationService,
)


class CreatePrivateConversationView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):

        recipient_id = request.data.get(
            "recipient_id"
        )

        conversation = (
            ConversationService.create_private_chat(
                request.user,
                recipient_id,
            )
        )

        serializer = ConversationSerializer(
            conversation
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )