from collections import defaultdict
from typing import Dict, Optional

from deps_message_flow.commands.common import Command
from deps_message_flow.commands.producer import CommandProducer

__all__ = ["FakeCommandProducer"]


class FakeCommandProducer(CommandProducer):
    def __init__(self, *args, **kwargs):
        self.channel_reply_commands: defaultdict[tuple[str, str], list[Command]] = defaultdict(list)

    def send(self, channel: str, command: Command, reply_to: str, *, headers: Optional[Dict[str, str]] = None) -> str:
        self.channel_reply_commands[channel, reply_to].append(command)
        return ""

    def reset_commands(self):
        self.channel_reply_commands: defaultdict[tuple[str, str], list[Command]] = defaultdict(list)
