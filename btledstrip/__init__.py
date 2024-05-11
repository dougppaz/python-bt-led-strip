"""
btledstrip module
"""
from typing import Any
from bleak import BleakClient
from .consts import (
    EXEC_PREFIX,
    COMMAND_PREFIX,
)
from .controllers import (
    BaseController,
    MELKController,
)

class BTLedStrip:
    """
    BTLedStrip class
    """
    def __init__(self,
                 controller: BaseController,
                 mac_address: str) -> None:
        self._controller = controller
        self._bt_client = BleakClient(mac_address)

    async def get_model_number(self) -> str:
        """
        get model number
        """
        async with self._bt_client as bt_client:
            model_number = await bt_client.read_gatt_char(self._controller.char_specifier)
            return model_number

    def __getattribute__(self, name: str) -> Any:
        if not name.startswith(EXEC_PREFIX):
            return super().__getattribute__(name)
        act = name.lstrip(EXEC_PREFIX)
        command = getattr(self._controller, f"{COMMAND_PREFIX}{act}")
        async def command_wrapper(**kwargs):
            async with self._bt_client as bt_client:
                await bt_client.write_gatt_char(
                    self._controller.char_specifier,
                    bytearray(command(**kwargs))
                )
        return command_wrapper

__all__ = [
    "BTLedStrip",
    "MELKController",
]
