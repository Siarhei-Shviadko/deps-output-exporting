from collections import defaultdict

from deps_message_flow.messaging.common import IMessage
from deps_message_flow.messaging.producer import IMessageProducer

__all__ = ["FakeMessageProducer"]


class FakeMessageProducer(IMessageProducer):
    def __init__(self, *args, **kwargs):
        self.channel_reply_commands: defaultdict[str, list[IMessage]] = defaultdict(list)

    def send(self, destination: str, message: IMessage) -> None:
        self.channel_reply_commands[destination].append(message)
