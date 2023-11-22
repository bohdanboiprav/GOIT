from faker import Faker
import pika

from models import Task

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

channel = connection.channel()

exchange_name = 'task_handler'
queue_name = 'task_queue2'

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name)


def create_task(task_quantity):
    for i in range(task_quantity):
        task = Task(fullname=Faker().name(),
                    email_address=Faker().email()).save()

        channel.basic_publish(exchange=exchange_name,
                              routing_key=queue_name,
                              body=str(task.id).encode(),
                              properties=pika.BasicProperties(
                                  delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                              ))

    connection.close()


if __name__ == '__main__':
    create_task(100)
