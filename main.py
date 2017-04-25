import echokit
from echokit import Response, PlainTextOutputSpeech, SimpleCard
from echokit import directives, audio_player

# In the Lambda config, 'handler' would be
# set to ``order_skill.handler``
handler = echokit.handler

# Your skill ID, as provided in the Alexa dev portal
echokit.verify_application_id = False


# All apps are required to handle three basic requests,
# which have their own decorators:
# * LaunchRequest:          @echokit.on_session_launch
# * SessionEndedRequest:    @echokit.on_session_end
# * IntentRequest:          @echokit.on_intent('your_intent_name')

# Handles: LaunchRequest
@echokit.on_session_launch
def session_started(request_wrapper):
    output_speech = PlainTextOutputSpeech("Welcome to Order Maker!")
    return Response(output_speech=output_speech)


# Handles: SessionEndedRequest
@echokit.on_session_end
def session_ended(request_wrapper):
    print(request_wrapper.request.reason)


# Handles: IntentRequest
@echokit.on_intent('HoursIntent')
def hours_intent(request_wrapper):
    output_speech = PlainTextOutputSpeech("We're open today from 5am to 8pm")
    return Response(output_speech=output_speech)


# Handles: IntentRequest
# This example is for an intent that handles a slot,
# showing how to access the intent's 'Order' slot.
# This would return output speech like: 'You asked me to jump'
# The session variable would be returned on the next invocation
@echokit.on_intent('OrderIntent')
def order_intent(request_wrapper):
    request = request_wrapper.request
    menu_item = request.intent.slots['MenuItem'].value
    response_text = f'You ordered: {menu_item}'
    card = SimpleCard(title="Order", content=response_text)
    return Response(output_speech=PlainTextOutputSpeech(response_text),
                    session_attributes={'last_order': menu_item},
                    card=card)


# Handles: IntentRequest (unimplemented intent)
# For example, if 'WeaveBasketIntent' is defined in your
# interaction model, but you haven't defined a handler
# for it with @echokit.on_intent('WeaveBasketIntent'),
# this will catch it. If you don't define your own here,
# by default echokit will return a "Sorry, I didn't
# understand your request" speech response.
@echokit.fallback
def unimplemented(request_wrapper):
    request = request_wrapper.request
    output_speech = PlainTextOutputSpeech(f"Sorry, {request.intent.name} "
                                          f"isn't implemented!")
    return Response(output_speech=output_speech)

0