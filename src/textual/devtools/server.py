from __future__ import annotations

import sys

from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_routedef import get
from aiohttp.web_ws import WebSocketResponse

from textual.devtools.client import DEFAULT_PORT
from textual.devtools.service import DevtoolsService

DEFAULT_SIZE_CHANGE_POLL_DELAY_SECONDS = 2


async def websocket_handler(request: Request) -> WebSocketResponse:
    """aiohttp websocket handler for sending data between devtools client and server

    Args:
        request (Request): The request to the websocket endpoint

    Returns:
        WebSocketResponse: The websocket response
    """
    service: DevtoolsService = request.app["service"]
    return await service.handle(request)


async def _on_shutdown(app: Application) -> None:
    """aiohttp shutdown handler, called when the aiohttp server is stopped"""
    service: DevtoolsService = app["service"]
    await service.shutdown()


async def _on_startup(app: Application) -> None:
    service: DevtoolsService = app["service"]
    await service.start()


def _run_devtools(port: int) -> None:
    app = _make_devtools_aiohttp_app()
    run_app(app, port=port)


def _make_devtools_aiohttp_app(
    size_change_poll_delay_secs: float = DEFAULT_SIZE_CHANGE_POLL_DELAY_SECONDS,
) -> Application:
    app = Application()

    app.on_shutdown.append(_on_shutdown)
    app.on_startup.append(_on_startup)

    app["service"] = DevtoolsService(
        update_frequency=size_change_poll_delay_secs,
    )

    app.add_routes(
        [
            get("/textual-devtools-websocket", websocket_handler),
        ]
    )

    return app


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = DEFAULT_PORT
    _run_devtools(port)
