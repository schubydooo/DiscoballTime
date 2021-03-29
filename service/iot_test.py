import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time


import yaml
import json
from types import SimpleNamespace

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.


# Using globals to simplify sample code

received_count = 0
received_all_event = threading.Event()

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def on_connection_interrupted(connection, error, **kwargs):
    '''
    Callback when connection is accidentally lost.
    '''
    print(f"Connection interrupted. error: {error}")


def on_connection_resumed(connection, return_code, session_present, **kwargs):
    '''
    Callback when an interrupted connection is re-established.
    '''
    print(f"Connection resumed. return_code: {return_code} session_present: {session_present}")

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)

def on_resubscribe_complete(resubscribe_future):
    '''
    Callback when ...
    '''
    resubscribe_results = resubscribe_future.result()
    print(f"Resubscribe results: {resubscribe_results}")

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit(f"Server rejected resubscribe to topic: {topic}")

def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    '''
    Callback when the subscribed topic receives a message
    '''
    print(f"Received message from topic '{topic}': {payload}")

if __name__ == '__main__':

    # Read in config
    with open("config.yaml", "r") as ymlfile:
        cfg = SimpleNamespace(**yaml.safe_load(ymlfile))

    # Spin up resources
    io.init_logging(getattr(io.LogLevel, io.LogLevel.NoLogs.name), 'stderr')
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)


    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=cfg.thing_endpoint,
        cert_filepath=cfg.cert,
        pri_key_filepath=cfg.priv_key,
        client_bootstrap=client_bootstrap,
        ca_filepath=cfg.root_ca,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=cfg.client_id,
        clean_session=False,
        keep_alive_secs=6)

    print(f"Connecting to {cfg.thing_endpoint} with client ID '{cfg.client_id}'...")
    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    # Subscribe
    print(f"Subscribing to topic '{cfg.topic}'...")
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=cfg.topic,
        qos=mqtt.QoS.AT_MOST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print(f"Subscribed with {str(subscribe_result['qos'])}")

    # Publish message to server desired number of times.
    # This step is skipped if message is blank.
    # This step loops forever if count was set to 0.
    publish_count = 1
    while (publish_count <= 2):
        message = json.dumps({'PublishCount': publish_count})
        print(f"Publishing message to topic '{cfg.topic}': {message}")
        mqtt_connection.publish(
            topic=cfg.topic,
            payload=message,
            qos=mqtt.QoS.AT_MOST_ONCE)
        time.sleep(1)
        publish_count += 1

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
