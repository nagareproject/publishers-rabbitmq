# --
# Copyright (c) 2008-2019 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""The RabbitMQ publisher"""

import time

from nagare.server import publisher


class Publisher(publisher.Publisher):
    """The RabbitMQ publisher"""

    CONFIG_SPEC = dict(publisher.Publisher.CONFIG_SPEC, channel='string')

    def __init__(self, name, dist, rabbitmq_service, services_service, **config):
        super(Publisher, self).__init__(name, dist, **config)

        self.rabbitmq = rabbitmq_service
        self.services = services_service

    def send(self, data):
        self.send_sock.send(data)

    def start_handle_request(self, app, **params):
        try:
            return super(Publisher, self).start_handle_request(app, **params)
        except Exception:
            return None

    def _serve(self, app, channel):
        rabbitmq_channel = self.services[channel]
        rabbitmq_channel.on_receive(
            lambda msg: self.start_handle_request(app, channel=rabbitmq_channel, msg=msg)
        )

        print time.strftime('%x %X -', time.localtime()), 'serving on channel', channel
        self.rabbitmq.start()

        return 0
