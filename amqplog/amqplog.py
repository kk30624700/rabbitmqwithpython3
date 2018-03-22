'''
Created on 2018年3月22日

@author: m24
'''
#-_- coding: UTF-8 -_-
import pika

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)

channel = conn_broker.channel() 

channel.queue_declare(queue="error_queue", passive=False, durable=False, exclusive=True, auto_delete=True)
channel.queue_declare(queue="warn_queue", passive=False, durable=False, exclusive=True, auto_delete=True)
channel.queue_declare(queue="info_queue", passive=False, durable=False, exclusive=True, auto_delete=True)

channel.queue_bind(queue="error_queue",
                   exchange="amq.rabbitmq.log",
                   routing_key="error")
channel.queue_bind(queue="warn_queue",
                   exchange="amq.rabbitmq.log",
                   routing_key="warning")
channel.queue_bind(queue="info_queue",
                   exchange="amq.rabbitmq.log",
                   routing_key="info")

def error_callback(channel, method, header, body):
    print("error: " + body.decode())
    channel.basic_ack(delivery_tag=method.delivery_tag)
    
def warn_callback(channel, method, header, body):
    print("warn: " + body.decode())
    channel.basic_ack(delivery_tag=method.delivery_tag)
    
def info_callback(channel, method, header, body):
    print("info: " + body.decode())
    channel.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_consume(consumer_callback=error_callback, queue="error_queue", consumer_tag="error_consumer")
channel.basic_consume(consumer_callback=warn_callback, queue="warn_queue", consumer_tag="warn_consumer")
channel.basic_consume(consumer_callback=info_callback, queue="info_queue", consumer_tag="info_consumer")

channel.start_consuming()    