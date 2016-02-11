# -*- coding: utf-8-*-
import logging
import paho.mqtt.publish as publish

INTENTS = ['lights', 'play_media', 'thermostat_set', 'scene_change']
# Required by brain.py
WORDS = INTENTS

PRIORITY = 1

MQTTHOST = "pixie"
TOPIC_ROOT = "ha/"
DEFAULT_LOC = "kitchen"
BAD_PARSE_MSG = "Oops. I couldn't understand that."


def handle(text, mic, profile):
    """
        Handle home automation events based on user input

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
        number)
    """
    if hasattr(text, 'tags') and len(text.tags) > 0:
        _handle_intent(text, mic, profile)


def _handle_intent(tagged_text, mic, profile):
    """
    Parse text with attached named-entity tree
    """

    def parse_room(tree):
        room = DEFAULT_LOC
        if 'room' in tree['entities'].keys():
            room = tree['entities']['room'][0]['value']
            if room == 'bedroom':
                # speaker dependent, can't interpolate
                room = 'unknown'
        return room

    def intent_to_mqtt_lights(tree):
        ents = tree['entities']
        room = parse_room(tree)
        item = None

        if 'light_group' in ents.keys():
            item = ents['light_group'][0]['value']
        elif 'light_item' in ents.keys():
            item = 'lights/' + ents['light_item'][0]['value']
            # FIXME: fix lights/amplifier intent mapping
            if item == 'lights/amplifier':
                item = 'amp'
        else:
            item = 'lights'

        if not item:
            return (None, None)

        if 'dimmer_level' in ents.keys():
            new_state = ents['dimmer_level'][0]['value']
        else:
            new_state = ents['on_off'][0]['value']
        topic = room + '/' + item
        return (topic, new_state)

    def intent_to_mqtt_media(tree):
        ents = tree['entities']
        room = parse_room(tree)
        item = 'media' + '/' + ents['media_action'][0]['value']
        new_state = 'on'

        if ents['media_action'][0]['value'] == 'volume':
            new_state = ents['volume_percent'][0]['value']

        topic = room + '/' + item
        return (topic, new_state)

    def intent_to_mqtt_thermostat(tree):
        ents = tree['entities']
        room = parse_room(tree)
        item = 'unknown'
        if 'temperature' in ents.keys():
            item = 'setpoint'
            new_state = ents['temperature'][0]['value']

        topic = room + '/' + item
        return (topic, new_state)

    def intent_to_mqtt_scene_change(tree):
        ents = tree['entities']
        room = parse_room(tree)
        item = 'scene'
        new_state = ents['scene'][0]['value']

        topic = room + '/' + item
        return (topic, new_state)

    tree = tagged_text.tags

    logger = logging.getLogger(__name__)
    logger.debug("handle_intent: got tree=" + str(tree))

    topic = None
    new_state = None

    try:
        if tree['intent'] == 'lights':
            (topic, new_state) = intent_to_mqtt_lights(tree)
        elif tree['intent'] == 'play_media':
            (topic, new_state) = intent_to_mqtt_media(tree)
        elif tree['intent'] == 'thermostat_set':
            (topic, new_state) = intent_to_mqtt_thermostat(tree)
        elif tree['intent'] == 'scene_change':
            (topic, new_state) = intent_to_mqtt_scene_change(tree)
    except:
        mic.say(BAD_PARSE_MSG)
    else:
        if topic and new_state:
            logger.debug("ha: publishing to " + TOPIC_ROOT + topic)
            # new_state could be int, here so force conversion
            state = str(new_state)
            publish.single(TOPIC_ROOT + topic, state.upper(),
                           hostname=MQTTHOST, client_id=DEFAULT_LOC)

            mic.say(topic.replace('/', ' ') + " " + state)
        else:
            mic.say(BAD_PARSE_MSG)


def isValid(text):
    """
        Returns True if input is HA-related

        Arguments:
        text -- user-input, typically transcribed speech
    """
    if hasattr(text, 'tags') and len(text.tags) > 0:
        return text.tags['intent'] in INTENTS
    return False

##--------------------------------------------------------------##
import unittest
import mock
from client import test_mic, taggedtext


class TestTaggedText(unittest.TestCase):
    DEFAULT_PROFILE = {
        'prefers_email': False,
        'location': 'Cape Town',
        'timezone': 'US/Eastern',
        'phone_number': '012344321'
    }

    TEST_MQTT = [
        {
            'description': "Test basic lights on",
            'query': {'intent': "lights", 'entities': {
                'on_off': [{'value': "ON"}]
            }},
            'topic': DEFAULT_LOC + "/lights",
            'value': "ON"
        },
        {
            'description': "Test dimmers",
            'query': {'intent': "lights", 'entities': {
                "light_group": [{"value": "dimmers"}],
                "dimmer_level": [{"value": 100, "type": "value"}],
            }},
            'topic': DEFAULT_LOC + "/dimmers",
            'value': "100"
        },
        {
            'description': "Test amplifier mapping",
            'query': {'intent': "lights", 'entities': {
                'light_item': [{'value': "amplifier"}],
                'on_off': [{'value': "ON"}]
            }},
            'topic': DEFAULT_LOC + "/amp",
            'value': "ON"
        },
        {
            'description': "Test media play",
            'query': {'intent': "play_media", 'entities': {
                'media_action': [{'value': "play"}]}},
            'topic': DEFAULT_LOC + "/media/play",
            'value': "ON"
        },
        {
            'description': "Test media volume",
            'query': {'intent': "play_media", 'entities': {
                'media_action': [{'value': "volume"}],
                "volume_percent": [{"value": 80}]}},
            'topic': DEFAULT_LOC + "/media/volume",
            'value': "80"
        },
        {
            'description': "Test thermostat setpoint",
            'query': {'intent': "thermostat_set", 'entities': {
                'temperature': [{'value': "20"}]}},
            'topic': DEFAULT_LOC + "/setpoint",
            'value': "20"
        },
        {
            'description': "Test scene change",
            'query': {'intent': "scene_change", 'entities': {
                'scene': [{'value': "0"}]}},
            'topic': DEFAULT_LOC + "/scene",
            'value': "0"
        },
        {
            'description': "Test location",
            'query': {'intent': "lights", 'entities': {
                'on_off': [{'value': "ON"}],
                "room": [{"value": "study", "metadata": ""}],
            }},
            'topic': "study/lights",
            'value': "ON"
        },
    ]

    def setUp(self):
        self.profile = self.DEFAULT_PROFILE
        self.send = False

    def run_conversation(self, query, inputs):
        """Generic method for spoofing conversation.

        Arguments:
        query -- The initial input to the server.
        inputs -- Additional input, if conversation is extended.

        Returns:
        The server's responses, in a list.
        """
        self.assertTrue(isValid(query))
        mic = test_mic.Mic(inputs)
        handle(query, mic, self.profile)
        return mic.outputs

    def test_empty(self):
        query = taggedtext.TaggedText("", {})
        self.assertFalse(isValid(query))

    def test_intents_fail(self):
        for intent in INTENTS:
            query = taggedtext.TaggedText(
                "", {"intent": intent, "entities": {}})
            inputs = []
            outputs = self.run_conversation(query, inputs)
            self.assertEqual(len(outputs), 1)
            self.assertEqual([BAD_PARSE_MSG], outputs)

    def test_mqtt(self):
        for t in self.TEST_MQTT:
            query = taggedtext.TaggedText("", t['query'])
            with mock.patch.object(publish, 'single') as mocked_publish:
                inputs = []
                outputs = self.run_conversation(query, inputs)
                mocked_publish.assert_called_once_with(
                    TOPIC_ROOT + t['topic'],
                    t['value'],
                    hostname=MQTTHOST,
                    client_id=DEFAULT_LOC)
            # Just ensure it says *something*
            self.assertEqual(len(outputs), 1)
