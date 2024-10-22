from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.api.v1.endpoints import auth
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME or "Authentication Service",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])


@app.get("/")
def read_root() -> dict:
    return {"message": "Welcome to the Authentication Service"}


# Add this debugging code
print("Registered routes:")
for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"Route: {route.path}, Methods: {route.methods}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=8001
    )  # Note: Using 8001 to avoid conflict with User MS
