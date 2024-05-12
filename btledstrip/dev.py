"""
Dev Command Terminal

Debug a controller sending programmatically commands via Bluetooth.

usage: python -m btledstrip.dev -h
"""
import argparse
import logging
import asyncio
from typing import Type
from btledstrip import (
    BTLedStrip,
    Controller,
    MELKController
)

logger = logging.getLogger(__name__)

CONTROLLERS_CLASS = {
    "melk": MELKController
}

class ControllerClassAction(argparse.Action):
    """
    argparse controller class action
    """
    def __call__(self, _, namespace, values, option_string=None) -> None:
        setattr(namespace, self.dest, CONTROLLERS_CLASS[values])

async def main(controller_class: Type[Controller], mac_address: str):
    """
    main
    """
    controller = controller_class()
    async with BTLedStrip(controller, mac_address) as led_strip:
        command_input = input("> ")
        while command_input != "exit":
            command_args = list(map(int, command_input.split()))
            try:
                await led_strip.exec_command(*command_args)
            except Exception as e:  # pylint: disable=W0718
                logger.error(e)
            command_input = input("> ")

parser = argparse.ArgumentParser(prog="btledstrip Dev Command Terminal",
                                 description="Debug a controller sending programmatically commands "
                                             "via Bluetooth")
parser.add_argument("--debug",
                    default=False,
                    action=argparse.BooleanOptionalAction)
parser.add_argument("controller_class",
                    choices=CONTROLLERS_CLASS,
                    action=ControllerClassAction)
parser.add_argument("mac_address")

if __name__ == "__main__":
    args = parser.parse_args()
    logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO))
    asyncio.run(main(args.controller_class, args.mac_address))
