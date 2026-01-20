import json
from flask import jsonify
from rabbitmq.messages import AIRequest, AIResponse

class RabbitMQConsumer:
    def __init__(self, channel, llm_agent, producer):
        self.channel = channel
        self.llm_agent = llm_agent
        self.producer = producer

        self.channel.queue_declare(queue="ai_requests", durable=True)

    def start(self):
        self.channel.basic_consume(
            queue="ai_requests",
            on_message_callback=self._callback
        )
        self.channel.start_consuming()

    def _callback(self, ch, method, properties, body):
        print("Received message from queue.")
        print(body)
        data = json.loads(body)
        request = AIRequest(**data)

        try:
            if request.type == "Chat":
                result = self.llm_agent.chat(message=request.prompt)
            elif request.type == "Upload":
                result = self.llm_agent.upload_file(file_path=request.prompt)
                
            print(f"Processed request {request.jobId} successfully.")
            print(f"Result: {result}")
            response = AIResponse(
                jobId=request.jobId,
                status="completed",
                result=result
            )
        except Exception as e:
            response = AIResponse(
                jobId=request.jobId,
                status="failed",
                error=str(e)
            )

        self.producer.publish_response(response.__dict__)
        ch.basic_ack(delivery_tag=method.delivery_tag)
