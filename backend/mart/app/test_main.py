import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.main import consume_events

@pytest.mark.asyncio
async def test_consume_events():
    consumer = AsyncMock()
    consumer.start = AsyncMock()
    consumer.stop = AsyncMock()
    consumer.__aiter__ = AsyncMock(return_value=iter([]))
    
    with pytest.raises(asyncio.CancelledError):
        await consume_events(consumer)
    
    consumer.start.assert_called_once()
    consumer.stop.assert_called_once()