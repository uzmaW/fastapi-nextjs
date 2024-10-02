import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from app.main import app
import asyncio

class MockAIOKafkaProducer:
    def __init__(self):
        self.sent_messages = []

    async def start(self):
        pass

    async def stop(self):
        pass

    async def send_and_wait(self, topic, value):
        self.sent_messages.append((topic, value))

@pytest.fixture
def client():
    mock_producer = MockAIOKafkaProducer()
    app.state.kafka_producer = mock_producer
    return TestClient(app), mock_producer

@pytest.mark.asyncio
async def test_root_endpoint_logging(client):
    client, mock_producer = client
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    
    # Wait for a short time to allow async logging to complete
    await asyncio.sleep(0.1)
    
    # Check if a log message was sent to Kafka
    assert len(mock_producer.sent_messages) > 0
    topic, message = mock_producer.sent_messages[0]
    assert topic == 'fastapi_logs'
    assert b"Accessed root endpoint" in message

@pytest.mark.asyncio
async def test_items_endpoint_logging(client):
    client, mock_producer = client
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42}
    
    # Wait for a short time to allow async logging to complete
    await asyncio.sleep(0.1)
    
    # Check if a log message was sent to Kafka
    assert len(mock_producer.sent_messages) > 0
    topic, message = mock_producer.sent_messages[-1]  # Get the last message
    assert topic == 'fastapi_logs'
    assert b"Accessed item endpoint with id: 42" in message

@pytest.mark.asyncio
async def test_request_logging_middleware(client):
    client, mock_producer = client
    response = client.get("/")
    assert response.status_code == 200
    
    # Wait for a short time to allow async logging to complete
    await asyncio.sleep(0.1)
    
    # Check if a log message for the request was sent to Kafka
    assert len(mock_producer.sent_messages) > 0
    topic, message = mock_producer.sent_messages[0]  # Get the first message
    assert topic == 'fastapi_logs'
    assert b"Received request: GET" in message
    assert b"http://testserver/" in message