from aiokafka import AIOKafkaProducer
import asyncio
from retry import retry
import order_pb2

producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')

@retry(tries=3, delay=2)
async def send_order(order):
    order_data = order.SerializeToString()
    await producer.send_and_wait("order-events", order_data)

async def create_order(order_id, product_id, quantity, user_id):
    order = order_pb2.OrderRequest(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        user_id=user_id
    )
    await send_order(order)

# Start the event loop to send order data
asyncio.run(create_order("123", "P001", 2, "U001"))
