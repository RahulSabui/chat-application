from django.db import transaction
from django.db.models import Count

from accounts.models import User

from chat.models import (
    Conversation,
    ConversationParticipant,
)


class ConversationService:

    @staticmethod
    @transaction.atomic
    def create_private_chat(
        creator,
        recipient_id,
    ):

        recipient = User.objects.get(
            id=recipient_id,
            is_active=True,
        )

        conversations = (
            Conversation.objects.filter(
                type=Conversation.ConversationType.PRIVATE
            )
            .annotate(
                total=Count("participants")
            )
            .filter(total=2)
            .prefetch_related("participants")
        )

        for conversation in conversations:

            ids = set(
                conversation.participants.values_list(
                    "user_id",
                    flat=True,
                )
            )

            if ids == {creator.id, recipient.id}:
                return conversation

        conversation = Conversation.objects.create(
            type=Conversation.ConversationType.PRIVATE,
            created_by=creator,
            participant_count=2,
        )

        ConversationParticipant.objects.bulk_create([
            ConversationParticipant(
                conversation=conversation,
                user=creator,
                role=ConversationParticipant.Role.OWNER,
            ),
            ConversationParticipant(
                conversation=conversation,
                user=recipient,
                role=ConversationParticipant.Role.MEMBER,
            ),
        ])

        return conversation
