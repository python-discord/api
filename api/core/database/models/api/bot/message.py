from collections.abc import Mapping
from typing import Any, NoReturn, Union

from sqlalchemy import ARRAY, BigInteger, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, validates

from api.core.database import Base


def validate_embed_fields(fields: dict) -> Union[bool, NoReturn]:
    """Raises a ValueError if any of the given embed fields is invalid."""
    field_validators = ("name", "value", "inline")

    required_fields = ("name", "value")

    for field in fields:
        if len(field.get("name")) > 256:
            raise ValueError("Embed field-name length reached max limit.")
        if len(field.get("value")) > 1024:
            raise ValueError("Embed field-value length reached max limit.")
        if not isinstance((value := field.get("inline")), bool):
            raise ValueError(f"This field must be of type bool, not {type(value)}.")

        if not isinstance(field, Mapping):
            raise ValueError("Embed fields must be a mapping.")

        if not all(required_field in field for required_field in required_fields):
            raise ValueError(
                f"Embed fields must contain the following fields: {', '.join(required_fields)}."
            )

        for field_name in field:
            if field_name not in field_validators:
                raise ValueError(f"Unknown embed field field: {field_name!r}.")
    return True


def validate_embed_footer(footer: dict[str, str]) -> Union[bool, NoReturn]:
    """Raises a ValueError if the given footer is invalid."""
    field_validators = (
        "text",
        "icon_url",
        "proxy_icon_url",
    )
    if len(footer.get("text")) < 1:
        raise ValueError("Footer text must not be empty.")
    elif len(footer.get("text")) > 2048:
        raise ValueError("Footer text length reached the max limit.")

    if not isinstance(footer, Mapping):
        raise ValueError("Embed footer must be a mapping.")

    for field_name in footer:
        if field_name not in field_validators:
            raise ValueError(f"Unknown embed footer field: {field_name!r}.")
    return True


def validate_embed_author(author: Any) -> Union[bool, NoReturn]:
    """Raises a ValueError if the given author is invalid."""
    field_validators = (
        "name",
        "url",
        "icon_url",
        "proxy_icon_url",
    )
    if len(author.get("name")) < 1:
        raise ValueError("Embed author name must not be empty.")
    elif len(author.get("name")) > 256:
        raise ValueError("Embed author name length reached the max limit.")

    if not isinstance(author, Mapping):
        raise ValueError("Embed author must be a mapping.")

    for field_name in author:
        if field_name not in field_validators:
            raise ValueError(f"Unknown embed author field: {field_name!r}.")
    return True


class Message(Base):
    """A message, sent somewhere on the Discord server."""

    __tablename__ = "api_message"

    # The message ID as taken from Discord.
    id = Column(BigInteger, primary_key=True)

    # The channel ID that this message was
    # sent in, taken from Discord.
    channel_id = Column(BigInteger, nullable=False)

    # The content of this message, taken from Discord.
    content = Column(String(4000), nullable=False)
    # Embeds attached to this message.
    embeds = Column(ARRAY(JSONB(astext_type=Text())), nullable=False)

    author_id = Column(
        ForeignKey(
            "api_user.id", deferrable=True, initially="DEFERRED", ondelete="CASCADE"
        ),
        nullable=False,
        index=True,
    )

    # Attachments attached to this message.
    attachments = Column(ARRAY(String(length=512)), nullable=False)

    # The author of this message.
    author = relationship("User", passive_deletes=True)

    @validates("id")
    def validate_message_id(self, _key: str, message_id: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided id is negative."""
        if message_id < 0:
            raise ValueError("Message IDs cannot be negative.")
        return message_id

    @validates("channel_id")
    def validate_mchannel_id(self, _key: str, channel_id: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided id is negative."""
        if channel_id < 0:
            raise ValueError("Channel IDs cannot be negative.")
        return channel_id

    @validates("embeds")
    def validate_embeds(
        self, _key: str, embeds: list[Mapping]
    ) -> Union[list[Mapping], NoReturn]:
        """
        Validate a JSON document containing an embed as possible to send on Discord.

        This attempts to rebuild the validation used by Discord
        as well as possible by checking for various embed limits so we can
        ensure that any embed we store here will also be accepted as a
        valid embed by the Discord API.
        """
        all_keys = {
            "title",
            "type",
            "description",
            "url",
            "timestamp",
            "color",
            "footer",
            "image",
            "thumbnail",
            "video",
            "provider",
            "author",
            "fields",
        }
        one_required_of = {"description", "fields", "image", "title", "video"}
        for embed in embeds:
            title = embed.get("title")
            if len(title) < 1:
                raise ValueError("Embed title must not be empty")
            elif len(title) > 256:
                raise ValueError("Reached max length of embed title")
            description = embed.get("description")
            if len(description) > 4096:
                raise ValueError("Reached max length of embed description")
            if (
                validate_embed_fields(embed.get("fields"))
                and validate_embed_author(embed.get("author"))
                and validate_embed_footer(embed.get("footer"))
            ):
                continue

            if not embed:
                raise ValueError("Tag embed must not be empty.")

            elif not isinstance(embed, Mapping):
                raise ValueError("Tag embed must be a mapping.")

            elif not any(field in embed for field in one_required_of):
                raise ValueError(
                    f"Tag embed must contain one of the fields {one_required_of}."
                )

            for required_key in one_required_of:
                if required_key in embed and not embed[required_key]:
                    raise ValueError(f"Key {required_key!r} must not be empty.")

            for field_name in embed:
                if field_name not in all_keys:
                    raise ValueError(f"Unknown field name: {field_name!r}")

        return embeds
