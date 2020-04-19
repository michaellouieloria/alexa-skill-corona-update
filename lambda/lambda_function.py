# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests
import inflection
from bs4 import BeautifulSoup

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say number of confirmed or recovered or deaths in country or worldwide. Example: number of confirmed in usa."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class NumberConfirmedIntentHandler(AbstractRequestHandler):
    """Handler for NumberConfirmed Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NumberConfirmedIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        country_value = ask_utils.get_slot_value(handler_input=handler_input, slot_name="country")
        case_value = ask_utils.get_slot_value(handler_input=handler_input, slot_name="cases")
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        
        if (country_value and case_value):
            country_value = {
                'usa': 'us',
                'united states': 'us',
                'united states of america': 'us',
                'united kingdom': 'uk',
                'uae': 'united-arab-emirates',
                'ivory coast': 'cote-d-ivoire',
                'palestine': 'state-of-palestine',
                'congo': 'democratic-republic-of-the-congo',
                'vietnam': 'viet-nam',
            }.get(country_value.lower(), country_value)

            if case_value in ['deaths', 'death', 'recovered', 'recovering', 'recover', 'confirmed', 'confirming', 'confirm']:
                try:
                    if country_value == 'worldwide':
                        response = requests.get("https://www.worldometers.info/coronavirus")
                    else:
                        response = requests.get("https://www.worldometers.info/coronavirus/country/{}".format(inflection.dasherize(country_value.lower())))
                        
                    soup = BeautifulSoup(response.text, 'html.parser')
                    figures = soup.find_all('div', id='maincounter-wrap')
                    
                    if case_value in ['confirmed', 'confirming', 'confirm']:
                        confirmed = figures[0].find('span').text
                        speak_output = "{} confirmed cases".format(confirmed)
                        
                    if case_value in ['deaths', 'death']:
                        deaths = figures[1].find('span').text
                        speak_output = "{} deaths".format(deaths)
                        
                    if case_value in ['recovered', 'recovering', 'recover']:
                        recovered = figures[2].find('span').text
                        speak_output = "{} recovered cases".format(recovered)                    
                    
                except:
                    speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class AboutIntentHandler(AbstractRequestHandler):
    """Handler for About Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AboutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Corona update developed by Michael Louie Loria"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say number of confirmed or recovered or deaths in country or worldwide. Example: number of confirmed in usa."

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
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

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
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
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
sb.add_request_handler(NumberConfirmedIntentHandler())
sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()