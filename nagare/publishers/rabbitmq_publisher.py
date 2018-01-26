# --
# Copyright (c) 2008-2018 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""The RabbitMQ publisher"""

import time

from nagare.server import publishers


class Publisher(publishers.Publisher):
    """The RabbitMQ publisher"""

    CONFIG_SPEC = {'channel': 'string'}

    def __init__(self, name, dist, rabbitmq_service, services_service, **config):
        super(Publisher, self).__init__(name, dist, **config)

        self.rabbitmq = rabbitmq_service
        self.services = services_service

    def send(self, data):
        self.send_sock.send(data)

    def _serve(self, app, channel):
        rabbitmq_channel = self.services[channel]
        rabbitmq_channel.on_receive(
            lambda msg: app(channel=rabbitmq_channel, msg=msg)
        )

        print time.strftime('%x %X -', time.localtime()), 'serving on channel', channel
        self.rabbitmq.start()

        return 0
