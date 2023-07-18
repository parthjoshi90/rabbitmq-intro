from amqp_client import RabbitmqClient

client = RabbitmqClient(exchange="Test")
client.connect()

order_data = {
    "order_name": "ORDER00001",
    "customer": "Test customer",
    "order_subtotal": 10000,
    "order_total": 10200,
    "tax_amount": 200,
    "order_status": "paid",
}

customer_data = {
    "customer_id": 21452136,
    "email": "abc@test.com",
}

if client.channel:
    client.publish_message(routing_key="customer.notify", body=customer_data)
    client.publish_message(routing_key="stock.notify", body=order_data)