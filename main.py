from fastapi import FastAPI
from passive_liveness_api.app.handlers import router

app = FastAPI(title="Passive Liveness API")
app.include_router(router)
