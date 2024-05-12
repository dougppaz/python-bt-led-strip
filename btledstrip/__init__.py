"""
btledstrip module
"""
from typing import Any
from bleak import BleakClient
from .consts import (
    EXEC_PREFIX,
    COMMAND_PREFIX,
)
from .controllers import MELKController

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
        self.mac_address = mac_address

    async def __aenter__(self) -> 'BTLedStrip':
        self._bt_client = BleakClient(self.mac_address)
        await self._bt_client.__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        await self._bt_client.__aexit__(*args)
        self._bt_client = None

    async def get_model_number(self) -> str:
        """
        get model number
        """
        assert self._bt_client
        model_number = await self._bt_client.read_gatt_char(self._controller.char_specifier)
        return model_number

    def __getattribute__(self, name: str) -> Any:
        if not name.startswith(EXEC_PREFIX):
            return super().__getattribute__(name)
        act = name.removeprefix(EXEC_PREFIX)
        command = getattr(self._controller, f"{COMMAND_PREFIX}{act}")
        async def command_wrapper(**kwargs):
            assert self._bt_client
            await self._bt_client.write_gatt_char(
                self._controller.char_specifier,
                bytearray(command(**kwargs))
            )
        return command_wrapper

__all__ = [
    "BTLedStrip",
    "MELKController",
]
