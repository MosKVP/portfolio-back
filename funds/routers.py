from fastapi import APIRouter
from fastapi.responses import JSONResponse
from funds.models import SearchResponse, NavResponse
from fastapi_cache.decorator import cache

import httpx

router = APIRouter(prefix="/funds")
base = "https://www.finnomena.com/fn3/api"


@router.get("/search")
async def search(q: str, size: int):
    url = f"{base}/search/fund/_search"
    params = {
        'q': q,
        'size': size
    }
    with httpx.Client() as client:
        response = client.get(url, params=params)
        if response.status_code == 200:
            return SearchResponse.parse_raw(response.read())
        else:
            return JSONResponse(response.json(),  response.status_code)


# TODO: should get only one day, but there's no api for that
@router.get("/{id}/nav")
@cache(expire=1*60*60)  # 1 hour
async def nav(id: str):
    url = f"{base}/fund/v2/public/funds/{id}/nav/q"
    params = {
        'range': 'MAX'
    }
    with httpx.Client() as client:
        response = client.get(url, params=params)
        if response.status_code == 200:
            return NavResponse.parse_raw(response.read())
        else:
            return JSONResponse(response.json(),  response.status_code)
