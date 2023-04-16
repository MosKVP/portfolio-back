from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

import httpx
import os

load_dotenv()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health")
def health_check():
    return "Healthy"


@app.get("/funds/{path:path}")
@app.post("/funds/{path:path}")
@limiter.limit("600/minute")
async def forward_request(request: Request, path: str):
    if path.startswith("FundDailyInfo/"):
        api_key = os.getenv('FUND_DAILY_INFO_KEY')
    elif path.startswith("FundFactsheet/"):
        api_key = os.getenv('FUND_FACTSHEET_KEY')
    else:
        raise HTTPException(status_code=404, detail="Not Found")

    url = f"https://api.sec.or.th/{path}"

    api_key = os.getenv('FUND_FACTSHEET_KEY')
    headers = {
        'ocp-apim-subscription-key': api_key
    }
    body = await request.json()
    with httpx.Client() as client:
        response = client.request(
            request.method, url, headers=headers, json=body)
        return JSONResponse(response.json(),  response.status_code)
