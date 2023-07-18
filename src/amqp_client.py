import pika
import json
from pika.channel import Channel


class RabbitmqClient:
    def __init__(self, host="localhost", port="5672", username="guest", password="guest", exchange="Test"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.exchange = exchange
        self._channel:Channel = False
        self._connection = False
        self.is_connected: bool = False
    
    @property
    def channel(self):
        return self._channel if (self._channel and self._channel.is_open) else False
    
    def connect(self) -> Channel:
        credentials = pika.PlainCredentials(
            username=self.username,
            password=self.password,
            erase_on_connect=False
        )
        params = pika.ConnectionParameters(
            host=self.host,
            credentials=credentials,
            port=self.port,
            heartbeat=10
        )
        connection = pika.BlockingConnection(parameters=params)
        self._channel:Channel = connection.channel()
        self._channel.exchange_declare(exchange=self.exchange, exchange_type="direct")
        self.is_connected = True
    
    def publish_message(self, routing_key:str=False, body:dict=dict()):
        self._channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=json.dumps(body)
        )
    
    def consume_message(self, queue, on_message_callback):
        self._channel.basic_consume(
            on_message_callback=on_message_callback,
            queue=queue
        )
