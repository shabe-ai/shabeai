import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())
        request.state.request_id = req_id            # stash it
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response 