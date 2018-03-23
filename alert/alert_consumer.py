'''
Created on 2018年3月22日

@author: m24
'''
#!/usr/bin/python3
#-_- coding: UTF-8 -_-
import json, smtplib
import pika
from multiprocessing.connection import deliver_challenge

def send_mail(recipients, subject, message):
    """E-mail generatork for received alerts"""
    
    headers = ("From: %s\r\nTO: \r\nDate: \r\n" + \
               "Subject: %s\r\n\r\n") % ("dream.m24.com", subject)
    smtp_server = smtplib.SMTP()
    smtp_server.connect("localhost", 25)
    smtp_server.sendmail("dream.m24.com", recipients, headers + str(message))
    
    smtp_server.close()
    
def critical_notify(channel, method, header, body):
    """Sends CRITICAL alerts  to administrators via e-mail"""
    EMAIL_RECIPS = ["abc@ef.com"]
    message = json.loads(body.decode())
    send_mail(EMAIL_RECIPS, "CRITICAL ALERT", message)
    print(("Send alert via email! Alert Text: %s " + \
           "Recipients: %s") % (str(message), str(EMAIL_RECIPS)))
    channel.basic_ack(deliver_tag=method.delivery_tag)

def rate_limit_notify(channel, method, header, body):
    """Sends RATE LIMIT alerts to adminstrators via e-mail"""
    EMAIL_RECIPS = ["abc@ef.com"]
    message = json.loads(body.decode())
    send_mail(EMAIL_RECIPS, "RATE LIMITED ALERT", message)
    print(("Send alert via email! Alert Text: %s " + \
          "Recipients: %s") % (str(message), str(EMAIL_RECIPS)))
    channel.basic_ack(deliverty_tag=method.delivery_tag)
    
if __name__=="__main__":
    AMQP_SERVER = "localhost"
    AMQP_USER = "alert_user"
    AMQP_PASS = "alert_user"
    AMQP_VHOST = "/"
    AMQP_EXCHANGE = "alerts"
    
    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
    conn_params = pika.ConnectionParameters(AMQP_SERVER,
                                            virtual_host=AMQP_VHOST,
                                            credentials=creds_broker)
    conn_broker = pika.BlockingConnection(conn_params)
    
    channel = conn_broker.channel()
    
    channel.exchange_declare(exchange=AMQP_EXCHANGE, exchange_type="topic", auto_delete=False)
    
    channel.queue_declare(queue="critical", auto_delete=False)
    channel.queue_bind(queue="critical", exchange=AMQP_EXCHANGE, routing_key="critical.*")
    
    channel.queue_declare(queue="rate_limit", auto_delete=False)
    channel.queue_bind(queue="rate_limit", exchange=AMQP_EXCHANGE, routing_key="*.alert")
    
    channel.basic_consume(critical_notify, queue="critical", no_ack=False, consumer_tag="critical")
    channel.basic_consume(rate_limit_notify, queue="rate_limit", no_ack=False, consumer_tag="rate_limit")
    
    print("Ready for alerts")
    
    channel.start_consuming()