from typing import List
from datetime import datetime
from pydantic import BaseModel


class Fund(BaseModel):
    id: str
    short_code: str
    name_th: str


class SearchResult(BaseModel):
    item: Fund


class SearchResponse(BaseModel):
    results: List[SearchResult]


class Nav(BaseModel):
    date: datetime
    value: float


class NavData(BaseModel):
    fund_id: str
    short_code: str
    navs: List[Nav]


class NavResponse(BaseModel):
    data: NavData
