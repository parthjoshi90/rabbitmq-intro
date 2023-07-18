from amqp_client import RabbitmqClient

client = RabbitmqClient()

client.connect()

def test_callback(ch, method, properties, body):
    print("\n\n\n>body>>>>>>?????????", body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

if client.channel:
    queue = client.channel.queue_declare("stock")
    queue_name = queue.method.queue
    client.channel.queue_bind(exchange="Test", routing_key="stock.notify", queue=queue_name)

    client.consume_message(queue_name, test_callback)
    client.channel.start_consuming()