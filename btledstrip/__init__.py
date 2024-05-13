"""
btledstrip module
"""
import logging
import asyncio
from typing import (
    Callable,
    Awaitable,
    Optional,
    Any,
)
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from .controllers import (
    Controller,
    MELKController,
    COMMAND_PREFIX,
)
from .typing import Command

logger = logging.getLogger(__name__)

class BTLedStripExec:  # pylint: disable=R0903
    """
    build BTLedStrip.exec
    """
    def __init__(self, bt_led_strip: "BTLedStrip") -> None:
        self._bt_led_strip = bt_led_strip

    def __getattr__(self, name: str) -> Callable[..., Awaitable[None]]:
        command_fn = getattr(self._bt_led_strip.controller, f"{COMMAND_PREFIX}{name}")
        assert command_fn
        async def command_wrapper(**kwargs):
            command = command_fn(**kwargs)
            await self._bt_led_strip.send_command(command)
            logger.info("exec %s %s successfully executed", name, kwargs)
        return command_wrapper

class BTLedStrip:
    """
    Create an object by passing the controller and its settings along with the bluethooth MAC
    address to control the LED strip.
    """
    exec: BTLedStripExec

    def __init__(self,
                 controller: Controller,
                 mac_address: str) -> None:
        self._controller = controller
        self._bt_client: Optional[BleakClient] = None
        self._characteristic = None
        self._mac_address = mac_address
        self.exec = BTLedStripExec(self)

    async def __aenter__(self) -> "BTLedStrip":
        self._bt_client = BleakClient(self._mac_address)
        await self.bt_client.__aenter__()
        for command in self._controller.init_commands():
            logger.info("%s send init command %s", self, command)
            await self.bt_client.write_gatt_char(
                self.characteristic,
                bytearray(command),
                False
            )
            await asyncio.sleep(1)
        logger.info("BTLedStrip context created %s", self)
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.bt_client.__aexit__(*args)
        self._bt_client = None
        self._characteristic = None
        logger.info("BTLedStrip context destroyed %s", self)

    @property
    def controller(self) -> Controller:
        """
        controller
        """
        return self._controller

    @property
    def bt_client(self) -> BleakClient:
        """
        bleak client
        """
        assert self._bt_client
        return self._bt_client

    @property
    def characteristic(self) -> BleakGATTCharacteristic:
        """
        write characteristic
        """
        if not self._characteristic:
            self._characteristic = self._bt_client.services.get_characteristic(
                self._controller.char_specifier)
        return self._characteristic

    async def send_command(self, command: Command):
        """
        send command via bluetooth
        """
        logger.debug("request %s write command: %s", self.bt_client, command)
        await self.bt_client.write_gatt_char(
            self.characteristic,
            bytearray(command),
            False
        )

    async def exec_command(self, *args: int) -> None:
        """
        exec command
        """
        command = self._controller.build_command(*args)
        await self.send_command(command)
        logger.info("command successfully executed: %s", args)

__all__ = [
    "BTLedStrip",
    "Controller",
    "MELKController",
    "Command",
]

VERSION = "0.1.1"
