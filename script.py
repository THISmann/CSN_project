import pika
import time

# RabbitMQ connection setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='ubuntu_log_queue')

# Function to tail logs
def follow(file):
    file.seek(0, 2)  # Go to the end of the file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)  # Sleep briefly and retry
            continue
        yield line

# Open the log file (syslog in this case)
with open("/var/log/syslog", "r") as logfile:
    loglines = follow(logfile)
    for line in loglines:
        # Publish each log line to RabbitMQ
        channel.basic_publish(exchange='',
                              routing_key='ubuntu_log_queue',
                              body=line)
        print(f"Sent log to RabbitMQ: {line.strip()}")

# Close connection
connection.close()