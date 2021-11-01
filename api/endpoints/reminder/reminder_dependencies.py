from fastapi import Depends

from .reminder_schemas import ReminderFilter


async def filter_values(reminder_filter: ReminderFilter = Depends()) -> dict:
    """Returns a dictionary exported from a ReminderFilter model from the Path, with None values excluded."""
    return reminder_filter.dict(exclude_none=True)
