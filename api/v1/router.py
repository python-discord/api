"""API routing and fallback logic."""
import http
import logging
from urllib.parse import urlparse

from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.routing import APIRouter
from httpx import AsyncClient

from api.core.settings import settings


log = logging.getLogger(__name__)
router = APIRouter(prefix='/api')


# Must be the last defined route.
@router.api_route('/{endpoint:path}')
async def proxy_to_old_api(endpoint: str, request: Request) -> Response:
    """
    Proxy the given request to the old API.

    Whilst the new API is in development, we will not immediately have all
    endpoints available for clients such as our bot to use.  That said, we also
    want to test the new API with live queries and incrementally migrate over
    services to use it instead of the old API.

    This function is a fallback route that is invoked by FastAPI when no other
    matching request handler could be found, and forwards the request, along
    with all headers (without some protocol specifics) to the old API. Any
    returned status code, headers, and body is then returned to the client
    as-is.

    Clients wishing to distinguish whether the request was handled directly
    by the new API or proxied to the old API can do so by introspecting the
    ``Via`` header returned in HTTP responses.
    """
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Via
    # We assume HTTP 1.1 here (we cannot know from the `Request` object).
    via_header = "HTTP/1.1 new-api"

    try:
        body = await request.body()
        # `.removeprefix()` is needed here until
        # https://github.com/python-discord/site/pull/526
        # is merged, as we mount the API router on the `/api` sub-path here.
        # The trailing slash from `/api` is removed to prevent issues due to double
        # slashes, such as `//api/healthcheck`.
        url = settings.old_api_endpoint + request.url.path.removeprefix('/api/')
        old_api_host = urlparse(settings.old_api_endpoint).netloc

        async with AsyncClient() as client:
            forward_response = await client.request(
                method=request.method,
                url=url,
                headers={
                    **request.headers,
                    # Host must be overwritten here, as the subdomain setup
                    # in the site dispatches to different URL configurations
                    # depending on the value specified here.
                    'Host': old_api_host,
                    # Authorization is also overwritten here, as we use our
                    # own authorization scheme that does not work with the
                    # old API. Users accessing the new API must authenticate
                    # using a separate token, anyways.
                    'Authorization': f'Token {settings.old_api_token}',
                    # Add a header here to indicate that we're accessing
                    # the API by proxy.
                    'Via': via_header,
                },
                params=request.query_params,
                cookies=request.cookies,
                content=body,
            )

        # The `Via` header added here is primarily for introspection
        # purposes by clients. For instance, we could create metrics
        # for the bot which would indicate which fraction of requests
        # is handled by the new API directly as compared to via the
        # old API. Note that setting the status code to the response
        # status code will also influence our access logs here.
        response = Response(
            content=forward_response.content,
            headers={
                **forward_response.headers,
                'Via': via_header,
            },
            status_code=forward_response.status_code,
        )

    except Exception as err:
        log.exception("Fatal error forwarding to old API:", exc_info=err)
        response = Response(
            content="Failed proxying request to the old API",
            # https://datatracker.ietf.org/doc/html/rfc7231.html#section-6.6.3
            status_code=http.HTTPStatus.BAD_GATEWAY,
            headers={'Via': via_header}
        )

    return response
