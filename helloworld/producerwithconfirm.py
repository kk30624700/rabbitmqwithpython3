'''
Created on 2018年3月21日

@author: m24
'''
#-_- coding: UTF-8 -_-

import pika, sys

credentials = pika.PlainCredentials("guest", "guest")
conn_params = pika.ConnectionParameters("localhost", credentials=credentials)
conn_broker = pika.BlockingConnection(conn_params)

channel = conn_broker.channel()
channel.confirm_delivery()

msg = "sys.argv[1]"
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

if channel.basic_publish(body=msg, properties=msg_props, routing_key="hola", exchange="hello-exchange"):
    print("Confirm received")
else:
    print("Message lost")
    
channel.close();
    