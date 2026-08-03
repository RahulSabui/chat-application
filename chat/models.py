import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True
class Conversation(BaseModel):

    class ConversationType(models.TextChoices):
        PRIVATE = "PRIVATE", "Private"
        GROUP = "GROUP", "Group"

    type = models.CharField(
        max_length=20,
        choices=ConversationType.choices,
        default=ConversationType.PRIVATE,
        db_index=True,
    )

    name = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="conversation_images/",
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_conversations",
    )

    # Message sequence generator
    last_sequence = models.BigIntegerField(
        default=0,
    )

    # Cached last message
    last_message = models.ForeignKey(
        "Message",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    last_message_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    participant_count = models.PositiveIntegerField(
        default=0,
    )

    is_archived = models.BooleanField(
        default=False,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:

        db_table = "conversations"

        ordering = ["-last_message_at", "-created_at"]

        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["created_by"]),
            models.Index(fields=["last_message_at"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):

        if self.type == self.ConversationType.PRIVATE:
            return f"Private Chat ({self.id})"

        return self.name or f"Group ({self.id})"
    
class ConversationParticipant(BaseModel):

    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        ADMIN = "ADMIN", "Admin"
        MEMBER = "MEMBER", "Member"

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="participants",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversation_participants",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )

    nickname = models.CharField(
        max_length=100,
        blank=True,
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    left_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_muted = models.BooleanField(
        default=False,
    )

    notification_enabled = models.BooleanField(
        default=True,
    )

    is_pinned = models.BooleanField(
        default=False,
    )

    joined_via_link = models.BooleanField(
        default=False,
    )

    last_read_message = models.ForeignKey(
        "Message",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    last_seen_message = models.ForeignKey(
        "Message",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:

        db_table = "conversation_participants"

        ordering = ["joined_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["conversation", "user"],
                name="unique_conversation_participant",
            )
        ]

        indexes = [
            models.Index(fields=["conversation"]),
            models.Index(fields=["user"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.conversation}"
    

class Message(models.Model):

    class MessageType(models.TextChoices):
        TEXT = "TEXT", "Text"
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"
        FILE = "FILE", "File"
        AUDIO = "AUDIO", "Audio"
        LOCATION = "LOCATION", "Location"
        CONTACT = "CONTACT", "Contact"
        SYSTEM = "SYSTEM", "System"

    class MessageStatus(models.TextChoices):
        SENT = "SENT", "Sent"
        DELIVERED = "DELIVERED", "Delivered"
        READ = "READ", "Read"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    type = models.CharField(
        max_length=20,
        choices=MessageType.choices,
        default=MessageType.TEXT,
    )

    content = models.TextField(blank=True)

    # -----------------------
    # NEW FIELDS START HERE
    # -----------------------

    sequence = models.BigIntegerField()

    status = models.CharField(
        max_length=20,
        choices=MessageStatus.choices,
        default=MessageStatus.SENT,
    )

    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="replies",
    )

    is_forwarded = models.BooleanField(default=False)

    forwarded_from = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="forwarded_messages",
    )

    is_edited = models.BooleanField(default=False)

    edited_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    is_deleted = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(default=dict)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        db_table = "messages"

        ordering = ["sequence"]

        indexes = [
            models.Index(fields=["conversation"]),
            models.Index(fields=["sender"]),
            models.Index(fields=["sequence"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["conversation", "sequence"]),
            models.Index(fields=["conversation", "created_at"]),
        ]

class MessageAttachment(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    file = models.FileField(
        upload_to="messages/",
    )

    file_name = models.CharField(
        max_length=255,
    )

    mime_type = models.CharField(
        max_length=100,
    )

    file_size = models.BigIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

class MessageReaction(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="reactions",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    emoji = models.CharField(
        max_length=20,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        unique_together = (
            "message",
            "user",
        )

class MessageRead(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="reads",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    read_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        unique_together = (
            "message",
            "user",
        )
