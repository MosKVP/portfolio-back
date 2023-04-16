from fastapi import FastAPI
from dotenv import load_dotenv
import funds.routers

load_dotenv()

app = FastAPI()
app.include_router(funds.routers.router)


@app.get("/health")
def health_check():
    return "Healthy"
