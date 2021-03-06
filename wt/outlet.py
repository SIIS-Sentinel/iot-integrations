from __future__ import division
from webthing import (Property, SingleThing, Thing, Value,
                      WebThingServer)
import logging
import paho.mqtt.client as mqtt

import config as cfg

from siisthing import SIISThing

from hardware.relay import Relay


class SIISOutlet(SIISThing):
    """A lock that logs received commands to stdout."""

    def __init__(self):
        SIISThing.__init__(
            self,
            "outlet_1",
            'urn:dev:siis:outlet',
            'My Outlet',
            ['SmartPlug'],
            'A web connected outlet'
        )

        self.state: Value = Value(False, self.set_value)
        self.add_property(
            Property(self,
                     'on',
                     self.state,
                     metadata={
                         '@type': 'OnOffProperty',
                         'title': 'On state',
                         'type': 'boolean',
                         'description': 'Whether the outlet is on',
                     }))

        self.device = Relay(cfg.pin)

    def on_message(self, client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
        if message.topic == self.scheduler_topic:
            # Stop the timer to prevent automatic changes
            self.auto_update = False
            payload: str = message.payload.decode()
            if payload == "ON":
                self.state.notify_of_external_update(True)
            elif payload == "OFF":
                self.state.notify_of_external_update(False)
        else:
            # Pass it down
            SIISThing.on_message(self, client, userdata, message)

    def set_value(self, value: bool) -> None:
        logging.debug(f"Outlet set to {'ON' if value else 'OFF'}")
        if value:
            self.device.on()
        else:
            self.device.off()


def run_server():
    thing = SIISOutlet()

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(SingleThing(thing), port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
