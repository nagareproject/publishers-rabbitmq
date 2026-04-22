# --
# Copyright (c) 2014-2026 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

"""The RabbitMQ publisher."""

from nagare.publishers import publisher


class Publisher(publisher.Publisher):
    """The RabbitMQ publisher."""

    CONFIG_SPEC = publisher.Publisher.CONFIG_SPEC | {
        'channel': 'string(help="name of the channel service to listen to")'
    }
    has_multi_threads = True

    def __init__(self, name, dist, rabbitmq_service, services_service, **config):
        super().__init__(name, dist, **config)

        self.rabbitmq = rabbitmq_service
        self.services = services_service

    def generate_banner(self):
        banner = super().generate_banner()
        return banner + ' on channel `{}`'.format(self.plugin_config['channel'])

    def _serve(self, app, channel, services_service, **conf):
        super()._serve(app)

        rabbitmq_channel = self.services[channel]
        rabbitmq_channel.on_receive(
            lambda msg: self.start_handle_request(app, services_service, channel=rabbitmq_channel, msg=msg)
        )

        try:
            rabbitmq_channel.start_consuming()
        except KeyboardInterrupt:
            rabbitmq_channel.stop_consuming()

        rabbitmq_channel.close()
        self.rabbitmq.close()

        return 0
