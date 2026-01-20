from rabbitmq.connection import create_connection
from rabbitmq.consumer import RabbitMQConsumer
from rabbitmq.producer import RabbitMQProducer
from agent import Agent

def main():
    agent = Agent()

    connection = create_connection("localhost")
    channel = connection.channel()

    producer = RabbitMQProducer(channel)
    consumer = RabbitMQConsumer(channel, agent, producer)

    print("AI Worker started. Waiting for messages...")
    consumer.start()

if __name__ == "__main__":
    main()
