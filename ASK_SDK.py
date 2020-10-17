# -*- coding: utf-8 -*-

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import pokedex as px

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

g_skill = None
g_poke = None
g_move = None


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Michael's pokedex skill! What would you like to do?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class TypeIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TypeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slot_value = get_spoken_value(handler_input.request_envelope.request, "Pokemon")
        poke = px.TypeIntent(slot_value)

        if not poke:
            return (
                handler_input.response_builder.speak("Please repeat the phrase").response
            )

        return (
            handler_input.response_builder
                .speak(poke)
                .ask("I didn't quite get that")
                .response
        )


class IDIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("IDIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slot_value = get_spoken_value(handler_input.request_envelope.request, "Poke")
        poke = px.pokemon_ID(slot_value)

        if not poke:
            return handler_input.response_builder.speak("Please repeat the phrase").response

        return (
            handler_input.response_builder
                .speak(poke)
                .ask("I didn't quite get that")
                .response)


class MoveIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MoveIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        poke_value = get_spoken_value(handler_input.request_envelope.request, "Poke")
        move_value = get_spoken_value(handler_input.request_envelope.request, "Move")

        poke = px.boolean_move(poke_value, move_value)

        return (
            handler_input.response_builder
                .speak(poke)
                .ask("I didn't quite get that")
                .response
        )


class DescriptionIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DescriptionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global g_skill, g_poke

        slot_value = get_spoken_value(handler_input.request_envelope.request, "Test")
        g_skill, g_poke = px.pokemon_description(slot_value)
        g_skill = "description"
        # just makes sure that the pokemon is readable in the next skill
        poke = px.pokemon_ID(slot_value)
        if not poke:
            return (
                handler_input.response_builder.speak("Please repeat the phrase").response
            )

        return (
            handler_input.response_builder
                .speak("Which game are you playing?")
                .ask("I didn't quite get that")
                .response
        )


class HowLearnMoveIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HowLearnMoveIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global g_poke, g_move, g_skill
        poke_value = get_spoken_value(handler_input.request_envelope.request, "Poke")
        move_value = get_spoken_value(handler_input.request_envelope.request, "Move")

        g_poke, g_move = px.how_move(poke_value, move_value)
        g_skill = "Move"
        if not g_poke or not g_move:
            return (
                handler_input.response_builder.speak("Please repeat the phrase").response
            )

        return (
            handler_input.response_builder
                .speak("Which game are you playing?")
                .ask("I didn't quite get that")
                .response
        )


class RepromptIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RepromptIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global g_skill, g_move, g_poke
        slot_value = get_spoken_value(handler_input.request_envelope.request, "Generation")
        response = px.game_version(slot_value, g_poke, g_move, g_skill)

        return (
            handler_input.response_builder
                .speak(response)
                .ask("I didn't quite get that")
                .response)


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can ask for a Pokemon's type, if or how they learn a move, their pokedex entry, or their ID number!"

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
        speak_output = "Thanks for using the skill!"

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

        speak_output = "Please repeat the phrase."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


def get_spoken_value(request, slot_name):
    if request.intent.slots[slot_name].slotValue["type"] == "List":
        return request.intent.slots[slot_name].slotValue["values"][0]["value"] + " " + \
               request.intent.slots[slot_name].slotValue["values"][1]["value"]
    else:
        return request.intent.slots[slot_name].value


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TypeIntentHandler())
sb.add_request_handler(IDIntentHandler())
sb.add_request_handler(MoveIntentHandler())
sb.add_request_handler(HowLearnMoveIntentHandler())
sb.add_request_handler(DescriptionIntentHandler())
sb.add_request_handler(RepromptIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# sb.add_request_handler(
#     IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()







