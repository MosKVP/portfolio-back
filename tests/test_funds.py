from funds.models import SearchResponse, NavResponse
from funds.routers import search, nav

import pytest

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_search():
    response = await search(q='USXNDQ', size=5)

    assert isinstance(response, SearchResponse)
    assert len(response.results) > 0


@pytest.mark.asyncio
async def test_nav():
    response = await nav(id='F0000143P4')

    assert isinstance(response, NavResponse)
    assert len(response.data.navs) > 0
