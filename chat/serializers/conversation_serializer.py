from rest_framework import serializers

from chat.models import (
    Conversation,
    ConversationParticipant,
)


class ParticipantSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:

        model = ConversationParticipant

        fields = (
            "id",
            "role",
            "nickname",
            "joined_at",
            "full_name",
        )

    def get_full_name(self, obj):

        return obj.user.get_full_name()
    
class ConversationSerializer(serializers.ModelSerializer):

    participants = ParticipantSerializer(
        many=True,
        read_only=True,
    )

    class Meta:

        model = Conversation

        fields = (
            "id",
            "type",
            "name",
            "description",
            "image",
            "participant_count",
            "last_message_at",
            "participants",
        )