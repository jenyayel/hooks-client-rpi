"""
Receieves notifications from remote queue.
"""

class Client(object):
    """Defines the client and all operations that can be performed on it"""

    def __init__(self, end_point, client_token):
        if not end_point:
            raise ValueError("'end_point' is required")

        if not client_token:
            raise ValueError("'client_token' is required")

    def start(self):
        """starts subscription"""
        pass

    def stop(self):
        """stops subscription"""
        pass

