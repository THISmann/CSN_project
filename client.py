import pika

def callback(ch, method, properties, body):
    print(f"Received {body}")

# Step 1: Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Step 2: Declare the queue you want to consume from
channel.queue_declare(queue='ubuntu_log_queue')

# Step 3: Set up subscription to the queue
channel.basic_consume(queue='ubuntu_log_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit, press CTRL+C')

# Step 4: Start consuming messages
channel.start_consuming()