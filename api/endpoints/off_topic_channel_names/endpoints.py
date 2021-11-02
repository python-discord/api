from typing import Optional, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Query, Session

from api.core.database.models.api.bot import OffTopicChannelName
from api.core.schemas import ErrorMessage
from api.endpoints.dependencies.database import create_database_session

otn = APIRouter(prefix="/off-topic-channel-names")


def get_all_otn(db_session: Session) -> Query:
    """Get a partial query object with .all()."""
    return db_session.query(OffTopicChannelName).all()


@otn.get(
    "/",
    status_code=200,
    response_model=list[str],
    responses={404: {"model": ErrorMessage}},
)
def get_off_topic_channel_names(
    random_items: Optional[int] = None,
    db_session: Session = Depends(create_database_session),
) -> Union[JSONResponse, list[str]]:
    """
    ### GET /bot/off-topic-channel-names.

    Return all known off-topic channel names from the database.

    If the `random_items` query parameter is given, for example using...
        $ curl 127.0.0.1:8000/api/bot/off-topic-channel-names?random_items=5
    ... then the API will return `5` random items from the database
    that is not used in current rotation.

    When running out of names, API will mark all names to not used and start new rotation.

    #### Response format
    Return a list of off-topic-channel names:
    >>> [
    ...     "lemons-lemonade-stand",
    ...     "bbq-with-bisk"
    ... ]

    #### Status codes
    - 200: returned on success
    - 400: returned when `random_items` is not a positive integer

    ## Authentication
    Requires a API token.
    """
    if not random_items:
        queryset = get_all_otn(db_session)
        return [offtopic_name.name for offtopic_name in queryset]

    if random_items <= 0:
        return JSONResponse(
            status_code=404,
            content={"error": ["'random_items' must be a positive integer."]},
        )

    queryset = get_all_otn(db_session).order_by("used", "?")[:random_items]

    # When any name is used in our listing then this means we reached end of round
    # and we need to reset all other names `used` to False
    if any(offtopic_name.used for offtopic_name in queryset):
        # These names that we just got have to be excluded from updating used to False
        get_all_otn(db_session).update(
            {
                OffTopicChannelName.used: OffTopicChannelName.name
                in (offtopic_name.name for offtopic_name in queryset)
            }
        )
    else:
        # Otherwise mark selected names `used` to True
        get_all_otn(db_session).filter_by(
            name__in=(offtopic_name.name for offtopic_name in queryset)
        ).update(used=True)

    return [offtopic_name.name for offtopic_name in queryset]


@otn.post(
    "/",
    status_code=201,
    responses={400: {"model": ErrorMessage}},
)
def create_off_topic_channel_names(
    name: str,
    db_session: Session = Depends(create_database_session),
) -> None:
    """
    ### POST /bot/off-topic-channel-names.

    Create a new off-topic-channel name in the database.
    The name must be given as a query parameter, for example:
        $ curl 127.0.0.1:8000/api/bot/off-topic-channel-names?name=lemons-lemonade-shop

    #### Status codes
    - 201: returned on success
    - 400: if the request body has invalid fields, see the response for details

    ## Authentication
    Requires a API token.
    """
    new_off_topic_channel_name = OffTopicChannelName(name=name)
    db_session.add(new_off_topic_channel_name)
    db_session.commit()


@otn.delete("/", status_code=204, responses={404: {"model": ErrorMessage}})
async def delete_off_topic_channel_names(
    name: str, db_session: Session = Depends(create_database_session)
) -> Optional[JSONResponse]:
    """
    ### DELETE /bot/off-topic-channel-names/<name:str>.

    Delete the off-topic-channel name with the given `name`.

    #### Status codes
    - 204: returned on success
    - 404: returned when the given `name` was not found

    ## Authentication
    Requires a API token.
    """
    if not (
        otn_to_delete := db_session.query(OffTopicChannelName)
        .filter_by(name=name)
        .first()
    ):
        return JSONResponse(
            status_code=404,
            content={
                "error": "There is no off topic channel name with that `name` in the database"
            },
        )
    db_session.delete(otn_to_delete)
    db_session.commit()
