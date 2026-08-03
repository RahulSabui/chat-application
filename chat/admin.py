from django.contrib import admin

from .models import (
    Conversation,
    ConversationParticipant,
    Message,
    MessageAttachment,
    MessageReaction,
    MessageRead,
)

admin.site.register(Conversation)
admin.site.register(ConversationParticipant)
admin.site.register(Message)
admin.site.register(MessageAttachment)
admin.site.register(MessageReaction)
admin.site.register(MessageRead)