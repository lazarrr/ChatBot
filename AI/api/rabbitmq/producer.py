import json

class RabbitMQProducer:
    def __init__(self, channel):
        self.channel = channel
        self.channel.queue_declare(queue="ai_responses", durable=True)

    def publish_response(self, response: dict):
        self.channel.basic_publish(
            exchange="",
            routing_key="ai_responses",
            body=json.dumps(response),
            properties=None
        )
