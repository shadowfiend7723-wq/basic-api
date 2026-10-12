from fastapi import FastAPI

from app.login import router as login_router
from app.register import router as register_router

app = FastAPI(title="NOVA API")
app.include_router(register_router)
app.include_router(login_router)


@app.get("/")
def index() -> dict[str, str]:
    return {"message": "NOVA API From master", "docs": "/docs"}