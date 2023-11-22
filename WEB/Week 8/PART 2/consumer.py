import pika
import sys

from models import Task


def send_email(recipient):
    print(f'Sending email to {recipient}')


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    queue = 'task_queue2'
    channel.queue_declare(queue=queue, durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        task = Task.objects(id=body.decode(), status=False).first()
        if task:
            send_email(task.email_address)
            task.update(set__status=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
