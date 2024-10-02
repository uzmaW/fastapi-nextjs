from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
import asyncio
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

async def consume_notifications():
    consumer = AIOKafkaConsumer(
        'notification-events',
        bootstrap_servers='kafka:9092',
        group_id="notification-group"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            # Decode message
            send_email("customer@example.com", "Order Update", msg.value.decode('utf-8'))
    finally:
        await consumer.stop()

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "noreply@order-system.com"
    msg['To'] = to_email
    with smtplib.SMTP('smtp-server:587') as server:
        server.sendmail("noreply@order-system.com", to_email, msg.as_string())

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_notifications())

