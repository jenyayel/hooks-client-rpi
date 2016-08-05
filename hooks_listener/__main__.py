#!/usr/bin/env python
"""
Main entry point to application when running client from shell
"""
from __future__ import print_function
import os
import sys
import signal
from lib.mq_client.client import Client

def main():
    """main entry point to application"""

    end_point = ""
    client_token = ""

    if "HOOKSCLIENTRPI_ENDPOINT" in os.environ:
        end_point = os.environ["HOOKSCLIENTRPI_ENDPOINT"]

    if "HOOKSCLIENTRPI_TOKEN" in os.environ:
        client_token = os.environ["HOOKSCLIENTRPI_TOKEN"]

    if not end_point or not client_token:
        print("Endpoint or/and client token not specified")
        sys.exit(1)

    clnt = Client(end_point, client_token)
    print("Hit 'Enter' or 'Ctr+C' to exit...\n")

    # handle graceful shutdown of mq consumer
    signal.signal(signal.SIGTERM, lambda signal, frame: _term_handler(clnt))

    clnt.start()
    try:
        # block main thread
        input("")
    except KeyboardInterrupt:
        pass

    clnt.stop()
    return 0

def _term_handler(consumer):
    """Handles SIGTERM"""
    consumer.stop()
    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main())
