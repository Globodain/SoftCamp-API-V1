"""
<!-- -| 
  
  * Softcamp is a registered trademark in Spain as SoftCamp Spain, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->
"""

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import RedirectResponse, Response
from fastapi.responses import HTMLResponse
from public.routes import router
from models._metadata import tags_metadata
import aiofiles

app = FastAPI(
    title="API Documentation",
    description="You can come back by <a href='/'>clicking here</a>",
    version="1.0.0",
    openapi_tags=tags_metadata,
    redirect_slashes=True,
    docs_url="/endpoints",
    redoc_url="/documentation",
    terms_of_service="/terms",
    contact={
        "name": "Support for developers",
        "email": "team@globodain.com",
    }
)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/", "/documentation", "/endpoints"]:
            if not "session" in request.cookies:
                return RedirectResponse(url="/account")
        response = await call_next(request)
        return response

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if response.status_code == 404:
            async with aiofiles.open('templates/errors/404.html', mode='r') as f:
                content = await f.read()
            return HTMLResponse(content=content, status_code=404)
        return response

app.add_middleware(AuthMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.include_router(router)