import sys
import yaml
import json
import time
import logging
import argparse
import RPi.GPIO as GPIO
from DRV8825 import DRV8825
from types import SimpleNamespace
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from KasaControl import KasaStrip

# This sample uses the Message Broker for AWS IoT to send and receive messages
# through an MQTT connection. On startup, the device connects to the server,
# subscribes to a topic, and begins publishing messages to that topic.
# The device should receive those same messages back from the message broker,
# since it is subscribed to that same topic.

# Using globals to simplify sample code


MOTOR_UP = "up"
MOTOR_DOWN = "down"

# Read in config
with open("config.yaml", "r") as ymlfile:
    cfg = SimpleNamespace(**yaml.safe_load(ymlfile))

POWER_STRIP_NAME = cfg.power_strip_name
DISCOLIGHTS_PLUG_NAME = cfg.discolights_plug_name
DISCOBALL_PLUG_NAME = cfg.discoball_plug_name

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
    )
logger = logging.getLogger()


def revolutions_to_steps(revolution_count, steps_per_revolution=200):
    '''
    Returns the # of steps necessary for that revolutions, based on the hardware set cycle of 200 steps/revolution
    '''
    return revolution_count * steps_per_revolution

def on_connection_interrupted(connection, error, **kwargs):
    '''
    Callback when connection is accidentally lost.
    '''
    logger.info(f"Connection interrupted. error: {error}")

def on_connection_resumed(connection, return_code, session_present, **kwargs):
    '''
    Callback when an interrupted connection is re-established.
    '''
    logger.info(f"Connection resumed. return_code: {return_code} session_present: {session_present}")

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        logger.info("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)

def on_resubscribe_complete(resubscribe_future):
    '''
    Callback when ...
    '''
    resubscribe_results = resubscribe_future.result()
    logger.info(f"Resubscribe results: {resubscribe_results}")

    for topic, qos in resubscribe_results['topics']:
        if qos is None:
            sys.exit(f"Server rejected resubscribe to topic: {topic}")

def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    '''
    Callback when the subscribed topic receives a message
    '''
    logger.info(f"MSG: Topic={topic}")

    if topic == 'discoPi/LowerDiscoball':
        logger.info(f"\tLowering discoball...")
        lower_discoball()
    elif topic == 'discoPi/RaiseDiscoball':
        logger.info(f"\tRaising discoball...")
        raise_discoball()
    elif topic == 'discoPi/ControlMotor':
        logger.info(f"\tPayload: {json.loads(payload)}")
        control_motor(payload)
    else:
        logger.error("Unimplemented topic")

def lower_discoball():
    '''
    Command to lower the discoball
    '''
    # Init Kasa smart strip 
    smartPlugs = KasaStrip(DISCOLIGHTS_PLUG_NAME, DISCOBALL_PLUG_NAME, POWER_STRIP_NAME)

    # Turn on lights
    smartPlugs.turn_on_plug(smartPlugs.discolight_plug)

    # Motor functions to lower the discoball
    Motor1.TurnStep(direction=MOTOR_UP, steps=revolutions_to_steps(1))
    Motor1.TurnStep(direction=MOTOR_DOWN, steps=revolutions_to_steps(1))
    Motor3.TurnStep(direction=MOTOR_UP, steps=revolutions_to_steps(1))
    Motor3.TurnStep(direction=MOTOR_DOWN, steps=revolutions_to_steps(1))

    # Start spinning the discoball
    smartPlugs.turn_on_plug(smartPlugs.discoball_plug)

def raise_discoball():
    '''
    Command to raise the discoball 
    '''
    # Init Kasa smart strip 
    smartPlugs = KasaStrip(DISCOLIGHTS_PLUG_NAME, DISCOBALL_PLUG_NAME, POWER_STRIP_NAME)

    # Stop spinning the discoball
    smartPlugs.turn_off_plug(smartPlugs.discoball_plug)

    Motor1.TurnStep(direction=MOTOR_UP, steps=revolutions_to_steps(1))
    Motor1.TurnStep(direction=MOTOR_DOWN, steps=revolutions_to_steps(1))
    Motor3.TurnStep(direction=MOTOR_UP, steps=revolutions_to_steps(1))
    Motor3.TurnStep(direction=MOTOR_DOWN, steps=revolutions_to_steps(1))

    # Turn off the lights
    smartPlugs.turn_off_plug(smartPlugs.discolight_plug)



def control_motor(payload):
    payload = json.loads(payload)
    try: 
        motor = payload['motor_number']
        revolutions = payload['revolutions']
        direction = payload['motor_direction']

        # Set motor
        if motor == 1:
            Motor = Motor1
        elif motor == 3:
            Motor = Motor3
        else:
            raise TypeError(f"Payload 'motor' was {payload['motor']}, but needs to be either 'Motor1' or 'Motor2'")

        # Move motor
        Motor.TurnStep(direction=direction, steps=revolutions_to_steps(int(revolutions)))

    except:
        logger.error("Issue parsing payload")
    

if __name__ == '__main__':

    # Read in config
    with open("config.yaml", "r") as ymlfile:
        cfg = SimpleNamespace(**yaml.safe_load(ymlfile))

    global power_strip_name
    global discolights_plug_name
    global discoball_plug_name 

    power_strip_name = cfg.power_strip_name
    discolights_plug_name = cfg.discolights_plug_name
    discoball_plug_name = cfg.discoball_plug_name

    # Spin up resources
    Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(0, 1, 2))
    Motor3 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(3, 4, 5))

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

    logger.info(f"Connecting to {cfg.thing_endpoint} with client ID '{cfg.client_id}'...")
    connect_future = mqtt_connection.connect()
    connect_future.result()     # Future.result() waits until a result is available
    logger.info("Connected!")

    # Subscribe to topics
    logger.info(f"Subscribing to topic '{cfg.topic}'...")
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=cfg.topic,
        qos=mqtt.QoS.AT_MOST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    logger.info(f"Subscribed with {str(subscribe_result['qos'])}")


    # Infinite loop while waiting for messages on our subscriptions
    try:
        while True:
            time.sleep(600)

    # Cleanup resources on exit
    finally:
        # Disconnect from AWS IOT
        logger.info("\nDisconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        logger.info("Disconnected!")

        # Reset Motors
        logger.info ("Stopping motors & resetting GPIO")
        Motor1.Stop()
        Motor2.Stop()
        GPIO.cleanup()


