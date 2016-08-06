"""
Receieves notifications from remote queue.
"""
from azure.servicebus import ServiceBusService

class Client(object):
    """Defines the client and all operations that can be performed on it"""

    def __init__(self, end_point, client_token):
        if not end_point:
            raise ValueError("'end_point' is required")

        if not client_token:
            raise ValueError("'client_token' is required")

        self.running = False
        self.sbs = ServiceBusService(end_point,
                                     shared_access_key_name="ListenFromTopic",
                                     shared_access_key_value=client_token)

    def start(self):
        """starts subscription"""
        self.running = True
        while self.running:
            msg = sbs.receive_subscription_message('DevSubscription', 'client1')
            print(msg)

    def stop(self):
        """stops subscription"""
        self.running = False

