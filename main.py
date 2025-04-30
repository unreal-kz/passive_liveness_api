from fastapi import FastAPI
from passive_liveness_api.api.routes import router

app = FastAPI(title="Passive Liveness API")
app.include_router(router)
