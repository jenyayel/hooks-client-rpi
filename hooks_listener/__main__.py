#!/usr/bin/env python
"""
Main entry point to application when running client from shell
"""
from __future__ import print_function
import os
import sys
import signal
from lib.service_bus.client import Client

def main():
    """main entry point to application"""

    sbs_namespace = ""
    access_key = ""

    if "HCR_SBS_NAMESPACE" in os.environ:
        sbs_namespace = os.environ["HCR_SBS_NAMESPACE"]

    if "HCR_SBS_ACCESS_KEY" in os.environ:
        access_key = os.environ["HCR_SBS_ACCESS_KEY"]

    if not sbs_namespace or not access_key:
        print("Namespace or shared access key are not specified")
        sys.exit(1)

    clnt = Client(sbs_namespace, access_key)
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
