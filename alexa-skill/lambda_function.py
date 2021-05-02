# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as alexa
# from awscrt import io, mqtt, auth, http
# from awsiot import mqtt_connection_builder
import boto3
import json 
# from botocore.exceptions import ClientError
import os 
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ENDPOINT_URL = os.environ['ENDPOINT_URL']

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return alexa.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Groovy man, let's get you started.  Say what you want, what you really really feel."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask(speak_output)
                .response
        )


class LowerDiscoballIntentHandler(AbstractRequestHandler):
    """Handler for Lower Discoball Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        '''
        Expecting payload like the following... #TODO
        '''
        return alexa.is_intent_name("LowerDiscoballIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Handling LowerDiscoballIntent...")
    
        # Send command to IoT Core
        iot_client = boto3.client('iot-data', region_name='us-west-2', endpoint_url=ENDPOINT_URL)
        payload = {
            "intent": "LowerDiscoball"
        }
        # Change topic, qos and payload
        response = iot_client.publish(
                topic='discoPi/LowerDiscoball',
                qos=1,
                payload=json.dumps(payload)
            )

        speak_output = "ahhhhhh right, get dancin fellers"
                
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class RaiseDiscoballIntentHandler(AbstractRequestHandler):
    """Handler for Raise Discoball Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        '''
        Expecting payload like the following... #TODO
        '''
        return alexa.is_intent_name("RaiseDiscoballIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Handling RaiseDiscoballIntent...")
    
        # Send command to IoT Core
        iot_client = boto3.client('iot-data', region_name='us-west-2', endpoint_url=ENDPOINT_URL)
        payload = {
            "intent": "RaiseDiscoball"
        }
        # Change topic, qos and payload
        response = iot_client.publish(
                topic='discoPi/RaiseDiscoball',
                qos=1,
                payload=json.dumps(payload)
            )
        speak_output = "ahh, you could keep groovin"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class ControlMotorIntentHandler(AbstractRequestHandler):
    """Handler for Control Motor Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        '''
        Expecting payload like the following:
        {
            "motor_number": Int in [1, 2]
            "motor_direction": String in ['up', 'down']
            "revolutions": Int > 0
        }
        '''
        return alexa.is_intent_name("ControlMotorIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("Handling ControlMotorIntent...")
        logger.info(f"userId: {alexa.get_user_id(handler_input=handler_input)}")
        
        # Extract params
        motor_number = alexa.get_slot_value(handler_input=handler_input, slot_name="motor_number")
        motor_direction = alexa.get_slot_value(handler_input=handler_input, slot_name="motor_direction")
        revolutions = alexa.get_slot_value(handler_input=handler_input, slot_name="revolutions")
        logger.info(f"motor_number: {motor_number}.  motor_direction: {motor_direction}.    revolutions: {revolutions}")
        
        # Validate input
        invalid = []
        if motor_number not in ["1","3"]:
            invalid.append("motor number")
        if motor_direction not in ['up', 'down']:
            invalid.append("motor direction")
        if int(revolutions) < 0 or int(revolutions) > 25:
            invalid.append("revolution count")

        if len(invalid) > 0:
            speak_output = "Sorry homie, that is not a valid"
            for val in invalid:
                speak_output += f" {val}"
        else:
            speak_output = "Yes shaudy!"

            # Send command to IoT Core
            iot_client = boto3.client('iot-data', region_name='us-west-2', endpoint_url=ENDPOINT_URL)
            payload = {
                "motor_number": int(motor_number),
                "motor_direction": motor_direction,
                "revolutions": int(revolutions)            
            }
            # Change topic, qos and payload
            response = iot_client.publish(
                    topic='discoPi/ControlMotor',
                    qos=1,
                    payload=json.dumps(payload)
                )
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return alexa.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say things like rotate motor 1 down 2 revolutions.  Or ask to get groovy, dingus."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (alexa.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                alexa.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "The party cannot stop!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return alexa.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return alexa.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = alexa.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ControlMotorIntentHandler())
sb.add_request_handler(LowerDiscoballIntentHandler())
sb.add_request_handler(RaiseDiscoballIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
