import json
import logging
import os

from confluent_kafka import Producer, Consumer
from datetime import datetime
from flask import Flask, jsonify, request
from marshmallow import ValidationError

from schema import MovieEventSchema, PaymentEventSchema, UserEventSchema

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

movie_event_schema = MovieEventSchema()
user_event_schema = UserEventSchema()
payment_event_schema = PaymentEventSchema()

producer = Producer({'bootstrap.servers': os.getenv('KAFKA_BROKERS')})
consumer = Consumer({'bootstrap.servers': os.getenv('KAFKA_BROKERS'),
                     'group.id': 'my-group',})

@app.route('/api/events/health')
def health():
    return jsonify({"status": True})

def delivery_report(err, msg):
    if err:
        app.logger.info(f"Delivery failed: {err}")
    else:
        app.logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Or obj.strftime("%Y-%m-%dT%H:%M:%S")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


@app.route('/api/events/movie', methods=['POST'])
def create_movie_event():
    try:
        data = movie_event_schema.load(request.get_json())

        app.logger.info("Creating movie event")
        producer.produce(
            topic='movie-events',
            value=json.dumps(data).encode('utf-8'),
            callback=delivery_report
        )
        producer.flush()

        consumer.subscribe(['movie-events'])
        consumer.poll(1.0)

    except ValidationError as err:
        return jsonify(err.messages), 400

    return jsonify({"status": "success"}), 201

@app.route('/api/events/user', methods=['POST'])
def create_user_event():
    try:
        data = user_event_schema.load(request.get_json())

        app.logger.info("Creating user event")
        producer.produce(
            topic='user-events',
            value=json.dumps(data, default=datetime_serializer).encode('utf-8'),
            callback=delivery_report
        )
        producer.flush()

        consumer.subscribe(['user-events'])
        consumer.poll(1.0)

    except ValidationError as err:
        return jsonify(err.messages), 400

    return jsonify({"status": "success"}), 201

@app.route('/api/events/payment', methods=['POST'])
def create_payment_event():
    try:
        data = payment_event_schema.load(request.get_json())

        app.logger.info("Creating payment event")
        producer.produce(
            topic='payment-events',
            value=json.dumps(data, default=datetime_serializer).encode('utf-8'),
            callback=delivery_report
        )
        producer.flush()

        consumer.subscribe(['payment-events'])
        consumer.poll(1.0)

    except ValidationError as err:
        return jsonify(err.messages), 400

    return jsonify({"status": "success"}), 201
