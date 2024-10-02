import os
import uuid
import asyncio
import json
import logging.handlers
import logging
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.responses import Response
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from celery import Celery
from contextlib import asynccontextmanager
from pythonjsonlogger import jsonlogger
from .db.models.user import User
from .db.models.inventory import InventoryItem
from .security.auth import create_access_token, get_current_user
from .config.mt_log_handler import KafkaLoggingHandler
from .routes.routes import routes_list
# --- Configuration ---
CELERY_BROKER = os.getenv('REDIS_HOST','redis://localhost:6379/0')  # Or another Celery broker
KAFKA_BOOTSTRAP_SERVERS  = KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:19092')
KAFKA_TOPIC = 'fastapi_logs'


# Configure logging to use syslog
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# kafka_handler = KafkaLoggingHandler(KAFKA_BROKER, KAFKA_TOPIC)
# logger.addHandler(kafka_handler)

# Configure logging
logger = logging.getLogger()
logHandler = logging.handlers.SysLogHandler(address='/dev/log')
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    #kafka_handler = KafkaLoggingHandler(app.state.kafka_producer, KAFKA_TOPIC)
    #logger.addHandler(kafka_handler)
    
    app.state.kafka_producer = get_kafka_producer()
    app.state.kafka_consumer = get_kafka_consumer()
    # Start consuming events
    app.state.consumer_task = asyncio.create_task(consume_events())
   
    yield
    
    # Shutdown
    app.state.consumer_task.cancel()
    
    await app.state.kafka_producer.stop()
    await app.state.kafka_consumer.stop()
    
app = FastAPI(lifespan=lifespan)

# --- Session Middleware ---
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    response = await call_next(request)
    
    if isinstance(response, JSONResponse):
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=False,  # Set to False if not using HTTPS
            samesite="strict",
            max_age=1800,  # 30 minutes
            expires=datetime.now(timezone.utc) + timedelta(minutes=30)
        )
    
    return response

# --- Routes ---
for route in routes_list:
    app.include_router(route)

# --- Kafka Producer ---

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    return producer

async def get_kafka_consumer():
      consumer = AIOKafkaConsumer(
        "order_placed",
        "order_confirmed",
        "order_shipped",
        "order_delivered",
        "order_cancelled",
        "payment_received",
        "payment_failed",
        "inventory_update",
        "product_added",
        "product_updated",
        "product_removed",
        "price_changed",
        "customer_registered",
        "customer_login",
        "customer_logout",
        "cart_updated",
        "wishlist_updated",
        "review_submitted",
        "return_requested",
        "refund_processed",
        "promotion_created",
        "promotion_ended",
        "low_stock_alert",
        "high_demand_alert",
        "supplier_shipment_received",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id='retail_group' 
      )
      await consumer.start()
      return consumer
# --- Auth ---
@app.post("/login")
def login(user: User):
    token = create_access_token({"username": user.username, "email": user.email})
    return {"access_token": token}

@app.get("/protected", dependencies=[Depends(get_current_user)])
def protected_route(user: Dict):
    return {"message": f"Welcome, {user['username']}! This is a protected route."}



@app.get("/")
async def root(request: Request):
    session_id = request.cookies.get("session_id", "No session ID")
    logger.info(f"Session ID: {session_id} , accessed root endpoint")
    return {"message": "hello ...", "session_id": session_id}

@app.get("/clear_session")
async def clear_session(response: Response):
    response.delete_cookie("session_id")
    return {"message": "Session cleared"}


# --- Celery App ---
celery_app = Celery(__name__, broker=CELERY_BROKER)

@celery_app.task
def send_email_task(email_data):
    # ... (Use an email library like smtplib or a service to send the email)

    print(f"Sending email: {email_data}")
    logger.info(f"Sending email: {email_data}")

# --- API Endpoints --- 
@app.post("/orders")
async def create_order(order_data: dict):
    producer = app.state.kafka_producer
    # Example order data with a unique order ID
    order_data['order_id'] = "order_123"  
    await producer.send_and_wait(
        "payment_received", 
        key=order_data['order_id'].encode(),  # Use order ID as the key
        value=json.dumps(order_data).encode()
    )
    return {"message": "Order created"}

@app.post("/inventory")
async def update_inventory(inventory_data: dict):
    producer = app.state.kafka_producer
    # Assuming inventory_data has a 'product_id'
    await producer.send_and_wait(
        "inventory_update",
        key=inventory_data['product_id'].encode(),  # Use product ID as key
        value=json.dumps(inventory_data).encode()
    )
    return {"message": "Inventory updated"}

# --- Kafka Consumers ---
async def consume_events():
  
    try:
        async for msg in app.state.kafka_consumer:
            if msg.topic == "payment_received":
                order_data = json.loads(msg.value.decode())
                print(f"Processing payment for order: {order_data['order_id']}")
                # ... (process payment logic, e.g., update order status in database)
                # Trigger email sending using Celery
                send_email_task.delay({
                    "to": "kodedsoft@gmail.com",
                    "subject": "Order Confirmation",
                    "body": f"Thank you for your order (ID: {order_data['order_id']})!"
                })

            elif msg.topic == "inventory_update":
                inventory_data = json.loads(msg.value.decode())
                print(f"Updating inventory for product: {inventory_data['product_id']}")
                # ... (update inventory in database, handle backorders, etc.)

            elif msg.topic == "send_email":  # Not used in this example, but shown for completeness
                email_data = json.loads(msg.value.decode())
                # ... (send the email - this would usually be handled by the send_email_task)
    except asyncio.CancelledError:
        # Handle cancellation
        logger.info("Consume events was cancelled")
    finally:
        await app.state.kafka_consumer.stop()


