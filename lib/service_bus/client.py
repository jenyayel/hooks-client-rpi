"""
Receieves notifications from remote queue.
"""
# pylint:disable=W0212
# pylint:disable=W0703

import threading
import logging
import json
from azure.servicebus import ServiceBusService

MESSAGE_WAIT_AFTER_ERROR = 5
MESSAGE_WAIT_TIMEOUT = 5
SBS_TOPIC_NAME = "webhooks"
SBS_SUBSCRIPTION_NAME = "RPiOneSubscription"
SBS_KEY_NAME = "ListenFromTopic"

class Client(object):
    """Client for ServiceBusService"""

    def __init__(self, sbs_namespace, sbs_access_key):
        if not sbs_namespace:
            raise ValueError("'sbs_namespace' is required")

        if not sbs_access_key:
            raise ValueError("'sbs_access_key' is required")

        self._logger = logging.getLogger(__name__)
        self._sbs = ServiceBusService(service_namespace=sbs_namespace,
                                      shared_access_key_name=SBS_KEY_NAME,
                                      shared_access_key_value=sbs_access_key)
        self._stop_event = None
        self._thread = None
        self._last_sequence = None

    def start(self):
        """starts subscription"""
        if not self._thread is None:
            raise Exception("Client already started")

        self._logger.info("Starting client for host %s", self._sbs._get_host())
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._receive_messages)
        self._thread.daemon = True
        self._thread.start()


    def stop(self):
        """stops subscription"""
        if self._thread is None:
            raise Exception("Client is not started")

        self._logger.info("Stopping client. May take up to %d seconds", MESSAGE_WAIT_TIMEOUT)
        self._stop_event.set()
        self._thread.join()
        self._thread = None
        self._stop_event = None
        self._logger.info("Client stopped")

    def _receive_messages(self):
        """Receieves messages from service"""
        while not self._stop_event.is_set():
            try:
                message = self._sbs.receive_subscription_message(SBS_TOPIC_NAME,
                                                                 SBS_SUBSCRIPTION_NAME,
                                                                 timeout=MESSAGE_WAIT_TIMEOUT,
                                                                 peek_lock=False)
            except Exception:
                self._logger.exception("Error while pulling message from topic")
                self._stop_event.wait(MESSAGE_WAIT_AFTER_ERROR)
                continue

            if message is None or message.body is None:
                self._logger.debug("No message received after waiting %d seconds",
                                   MESSAGE_WAIT_TIMEOUT)
            else:
                sequence = message.broker_properties[u'SequenceNumber']
                sent_on = message.broker_properties[u'EnqueuedTimeUtc']
                body = message.body
                self._logger.info("Message with sequence '%s' sent on '%s' receieved: %s",
                                  sequence, sent_on, body)
                if self._last_sequence > sequence:
                    self._logger.warning("Skipping message with sequence '%s' because the later"\
                                         " one with sequence '%s' was already processed",
                                         sequence, self._last_sequence)
                else:
                    self._last_sequence = sequence
                    try:
                        self._process_message(body)
                    except Exception:
                        self._logger.exception("Failed to process a message")


    def _process_message(self, message_body):
        """Process single message"""
        parsed_message = json.loads(message_body)
        msg_sender = parsed_message[u'name']
        msg_text = parsed_message[u'text']
        msg_type = parsed_message[u'type']
        if not msg_sender or not  msg_text or not msg_type:
            raise ValueError("One of requried parameters is missing")




