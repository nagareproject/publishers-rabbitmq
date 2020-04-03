# --
# Copyright (c) 2008-2020 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""The RabbitMQ publisher"""

from nagare.server import publisher


class Publisher(publisher.Publisher):
    """The RabbitMQ publisher"""

    CONFIG_SPEC = dict(
        publisher.Publisher.CONFIG_SPEC,
        channel='string(help="name of the channel service to listen to")'
    )
    has_multi_threads = True

    def __init__(self, name, dist, rabbitmq_service, services_service, **config):
        super(Publisher, self).__init__(name, dist, **config)

        self.rabbitmq = rabbitmq_service
        self.services = services_service

    def generate_banner(self):
        banner = super(Publisher, self).generate_banner()
        return banner + ' on channel `{}`'.format(self.plugin_config['channel'])

    def _serve(self, app, channel, **conf):
        super(Publisher, self)._serve(app)

        rabbitmq_channel = self.services[channel]
        rabbitmq_channel.on_receive(
            lambda msg: self.start_handle_request(app, channel=rabbitmq_channel, msg=msg)
        )

        try:
            rabbitmq_channel.start_consuming()
        except KeyboardInterrupt:
            rabbitmq_channel.stop_consuming()

        rabbitmq_channel.close()
        self.rabbitmq.close()

        return 0
