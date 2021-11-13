from typing import Optional, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database.models.api.bot import Reminder, User
from api.core.schemas import ErrorMessage
from api.endpoints.dependencies.database import create_database_session
from .reminder_dependencies import filter_values
from .reminder_schemas import ReminderCreateIn, ReminderPatchIn, ReminderResponse

reminder = APIRouter(prefix="/reminders")


@reminder.get(
    "/",
    status_code=200,
    response_model=list[ReminderResponse],
    response_model_by_alias=False,
    responses={404: {"model": ErrorMessage}},
)
async def get_reminders(
        db_session: AsyncSession = Depends(create_database_session),
        db_filter_values: dict = Depends(filter_values),
) -> Union[JSONResponse, list[ReminderResponse], None]:
    """
    ### GET /bot/reminders.

    Returns all reminders in the database.
    #### Response format
    >>> [
    ...     {
    ...         'active': True,
    ...         'author': 1020103901030,
    ...         'mentions': [
    ...             336843820513755157,
    ...             165023948638126080,
    ...             267628507062992896
    ...         ],
    ...         'content': "Make dinner",
    ...         'expiration': '5018-11-20T15:52:00Z',
    ...         'id': 11,
    ...         'channel_id': 634547009956872193,
    ...         'jump_url': "https://discord.com/channels/<guild_id>/<channel_id>/<message_id>",
    ...         'failures': 3
    ...     },
    ...     ...
    ... ]
    #### Status codes
    - 200: returned on success
    ## Authentication
    Requires an API token.
    """
    if not db_filter_values:
        if not (results := (await db_session.execute(select(Reminder))).scalars().all()):
            return []
        return results
    elif not (filtered_results := (await db_session.execute(
            select(Reminder).
            filter_by(**db_filter_values))
    ).scalars().all()):
        return JSONResponse(
            status_code=404,
            content={
                "error": "There are no reminders with the specified filter values."
            },
        )
    else:
        return filtered_results


@reminder.get(
    "/{reminder_id}",
    status_code=200,
    response_model=ReminderResponse,
    response_model_by_alias=False,
    responses={404: {"model": ErrorMessage}},
)
async def get_reminder_by_id(
        reminder_id: int, db_session: AsyncSession = Depends(create_database_session)
) -> Union[JSONResponse, ReminderResponse]:
    """
    ### GET /bot/reminders/<id:int>.

    Fetches the reminder with the given id.
    #### Response format
    >>>
    ... {
    ...     'active': True,
    ...     'author': 1020103901030,
    ...     'mentions': [
    ...         336843820513755157,
    ...         165023948638126080,
    ...         267628507062992896
    ...     ],
    ...     'content': "Make dinner",
    ...     'expiration': '5018-11-20T15:52:00Z',
    ...     'id': 11,
    ...     'channel_id': 634547009956872193,
    ...     'jump_url': "https://discord.com/channels/<guild_id>/<channel_id>/<message_id>",
    ...     'failures': 3
    ... }
    #### Status codes
    - 200: returned on success
    - 404: returned when the reminder doesn't exist
    ## Authentication
    Requires an API token.
    """
    if not (result := (await db_session.execute(select(Reminder).filter_by(id=reminder_id))).scalars().first()):
        return JSONResponse(
            status_code=404,
            content={"error": "There is no reminder in the database with that id!"},
        )
    return result


@reminder.patch(
    "/{reminder_id}",
    status_code=200,
    responses={404: {"model": ErrorMessage}, 400: {"model": ErrorMessage}},
)
async def edit_reminders(
        reminder_id: int,
        reminder_patch_in: ReminderPatchIn,
        db_session: AsyncSession = Depends(create_database_session),
) -> Optional[JSONResponse]:
    """
    ### PATCH /bot/reminders/<id:int>.

    Update the user with the given `id`.
    All fields in the request body are optional.
    #### Request body
    >>> {
    ...     'mentions': list[int],
    ...     'content': str,
    ...     'expiration': str,  # ISO-formatted datetime
    ...     'failures': int
    ... }
    #### Status codes
    - 200: returned on success
    - 400: if the body format is invalid
    - 404: if no user with the given ID could be found
    ## Authentication
    Requires an API token.
    """
    if not (await db_session.execute(select(Reminder).filter_by(id=reminder_id))).scalars().first():
        return JSONResponse(
            status_code=404,
            content={"error": "There is no reminder with that id in the database!"},
        )
    await db_session.execute(
        update(Reminder).where(Reminder.id == reminder_id).values(**reminder_patch_in.dict(exclude_none=True))
    )
    await db_session.commit()


@reminder.post(
    "/",
    status_code=201,
    responses={404: {"model": ErrorMessage}, 400: {"model": ErrorMessage}},
)
async def create_reminders(
        reminder_in: ReminderCreateIn,
        db_session: AsyncSession = Depends(create_database_session),
) -> Optional[JSONResponse]:
    """
    ### POST /bot/reminders.

    Create a new reminder.
    #### Request body
    >>> {
    ...     'author': int,
    ...     'mentions': list[int],
    ...     'content': str,
    ...     'expiration': str,  # ISO-formatted datetime
    ...     'channel_id': int,
    ...     'jump_url': str
    ... }
    #### Status codes
    - 201: returned on success
    - 400: if the body format is invalid
    - 404: if no user with the given ID could be found
     ## Authentication
    Requires an API token.
    """
    if not (await db_session.execute(select(User).filter_by(id=reminder_in.author_id))).scalars().first():
        return JSONResponse(
            status_code=404,
            content={"error": "There is no user with that id in the database!"},
        )
    new_reminder = Reminder(**reminder_in.dict())
    db_session.add(new_reminder)
    await db_session.commit()


@reminder.delete(
    "/{reminder_id}", status_code=204, responses={404: {"model": ErrorMessage}}
)
async def delete_reminders(
        reminder_id: int, db_session: AsyncSession = Depends(create_database_session)
) -> Optional[JSONResponse]:
    """
    ### DELETE /bot/reminders/<id:int>.

    Delete the reminder with the given `id`.
    #### Status codes
    - 204: returned on success
    - 404: if a reminder with the given `id` does not exist
    ## Authentication
    Requires an API token.
    """
    if not (reminder_to_delete := (await db_session.execute(
            select(Reminder).
            filter_by(id=reminder_id))
    ).scalars().first()):
        return JSONResponse(
            status_code=404,
            content={"error": "There is no reminder with that id in the database"},
        )
    await db_session.delete(reminder_to_delete)
    await db_session.commit()
