#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import requests
from config import SERVER, conf

if __name__ == "__main__":
    credentials = pika.PlainCredentials(SERVER['username'], SERVER['password'])
    parameters = pika.ConnectionParameters(SERVER['addr'], SERVER['port'], SERVER['path'], credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare('1c.fanout', exchange_type='fanout', durable=True)

    channel.queue_declare('tmall', passive=False, durable=True)
    channel.queue_bind('tmall', '1c.fanout')

    def get_products():
        url = conf['share_data']['goods']
        r = requests.get(url)
        if r.status_code == 200:
            return r.content
        raise Exception

    data = get_products()
    channel.basic_publish(exchange='1c.fanout', routing_key='', body=data)
    print " [x] Sent"

    connection.close()
