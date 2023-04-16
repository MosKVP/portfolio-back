from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from dotenv import load_dotenv
import funds.routers

load_dotenv()

app = FastAPI()
app.include_router(funds.routers.router)


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


@app.get("/health")
def health_check():
    return "Healthy"
