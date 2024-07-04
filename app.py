from fastapi import FastAPI, Request
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

from public.routes import router
from models._metadata import tags_metadata

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

# Comprobamos si el usuario tiene acceso a las rutas
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/", "/documentation", "/endpoints"]:
            # Aquí debes implementar tu lógica de autenticación.
            # Por ejemplo, puedes comprobar si hay una cookie de sesión válida:
            print("Entra aquí")
            print(request.cookies)
            if not "session" in request.cookies:
                print("Entra en not cookies")
                # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
                return RedirectResponse(url="/account")
        response = await call_next(request)
        return response

app.add_middleware(AuthMiddleware)
app.include_router(router)