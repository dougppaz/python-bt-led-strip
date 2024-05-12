"""
btledstrip module
"""
import logging
import asyncio
from typing import Any
from bleak import BleakClient
from .consts import (
    EXEC_PREFIX,
    COMMAND_PREFIX,
)
from .controllers import MELKController

logger = logging.getLogger(__name__)

class BTLedStrip:
    """
    Create an object by passing the controller and its settings along with the bluethooth MAC
    address to control the LED strips.
    """
    def __init__(self,
                 controller: MELKController,
                 mac_address: str) -> None:
        self._controller = controller
        self._bt_client = None
        self._characteristic = None
        self.mac_address = mac_address

    async def __aenter__(self) -> 'BTLedStrip':
        self._bt_client = BleakClient(self.mac_address)
        await self._bt_client.__aenter__()
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

    async def __aexit__(self, *args) -> None:
        await self._bt_client.__aexit__(*args)
        self._bt_client = None
        self._characteristic = None
        logger.info("BTLedStrip context destroyed %s", self)

    @property
    def bt_client(self) -> BleakClient:
        """
        bleak client
        """
        assert self._bt_client
        return self._bt_client

    @property
    def characteristic(self):
        """
        write characteristic
        """
        if not self._characteristic:
            self._characteristic = self._bt_client.services.get_characteristic(
                self._controller.char_specifier)
        return self._characteristic

    def __getattribute__(self, name: str) -> Any:
        if not name.startswith(EXEC_PREFIX):
            return super().__getattribute__(name)
        act = name.removeprefix(EXEC_PREFIX)
        command_fn = getattr(self._controller, f"{COMMAND_PREFIX}{act}")
        async def command_wrapper(**kwargs):
            command = command_fn(**kwargs)
            logger.debug("exec %s %s command: %s", act, kwargs, command)
            await self.bt_client.write_gatt_char(
                self.characteristic,
                bytearray(command),
                False
            )
            logger.info("exec %s %s successfully executed", act, kwargs)
        return command_wrapper

__all__ = [
    "BTLedStrip",
    "MELKController",
]
