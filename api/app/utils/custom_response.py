from fastapi.responses import Response
import anyio
import mimetypes
import os
from motor.motor_asyncio import AsyncIOMotorGridOut
from urllib.parse import quote
from starlette.types import Receive, Scope, Send
from starlette.background import BackgroundTask

### customized file response from https://github.com/encode/starlette/blob/master/starlette/responses.py for use with gridFS ###
class AsyncIOMotorFileResponse(Response):
    def __init__(
        self,
        grid_out: AsyncIOMotorGridOut,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None, 
        filename: str | None = None,
        content_disposition_type: str = "attachment",
    ) -> None:

        self.grid_out = grid_out
        self.status_code = status_code
        self.filename = filename if filename is not None else self.grid_out.filename

        if media_type is None:
            media_type = mimetypes.guess_type(self.filename)[0] or "text/plain"
        self.media_type = media_type
        self.background = background
        self.init_headers(headers)
        content_disposition_filename = quote(self.filename)
        if content_disposition_filename != self.filename:
            content_disposition = "{}; filename*=utf-8''{}".format(
                content_disposition_type, content_disposition_filename
            )
        else:
            content_disposition = '{}; filename="{}"'.format(
                content_disposition_type, self.filename
            )
        self.headers.setdefault("content-disposition", content_disposition)
        self.set_stat_headers()

    def set_stat_headers(self) -> None:
        content_length = str(self.grid_out.length)
        self.headers.setdefault('content-length', content_length)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )
        total = 0
        more_body = True
        while more_body:
            chunk = await self.grid_out.readchunk()
            total += len(chunk)
            more_body = total <= self.grid_out.length
            if not chunk:
                break
            await send(
                {
                    "type": "http.response.body",
                    "body": chunk,
                    "more_body": more_body
                }
            )
        if self.background is not None:
            await self.background()