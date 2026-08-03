from django.db import transaction
from django.db.models import Max

from chat.models import (
    Conversation,
    Message,
)


class MessageService:

    @staticmethod
    @transaction.atomic
    def send_text_message(
        conversation,
        sender,
        content,
    ):

        last_sequence = (
            Message.objects
            .filter(conversation=conversation)
            .aggregate(Max("sequence"))
            .get("sequence__max")
        )

        sequence = (last_sequence or 0) + 1

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content,
            sequence=sequence,
            status=Message.MessageStatus.SENT,
        )

        conversation.last_message = message
        conversation.last_message_at = message.created_at

        conversation.save(
            update_fields=[
                "last_message",
                "last_message_at",
            ]
        )

        return message