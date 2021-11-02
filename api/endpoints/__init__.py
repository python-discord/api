"""
Endpoint definitions of the Python Discord API.

This package contains all the route definitions of the Python Discord API.
There are currently no plan to use a strictly versioned API design, as this API
is currently tightly coupled with a single client application.
"""
from fastapi import APIRouter

from .off_topic_channel_names.endpoints import otn
from .reminder.reminder_endpoints import reminder

bot_router = APIRouter(prefix="/bot")

bot_router.include_router(reminder)
bot_router.include_router(otn)
