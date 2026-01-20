import pika

def create_connection(host: str = "rabbitmq") -> pika.BlockingConnection:
    credentials = pika.PlainCredentials("guest", "guest")
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=5672,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
    )
