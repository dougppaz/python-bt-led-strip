"""
controllers

supported controllers:
- MELK: MELKController

inspired by:
- https://github.com/dave-code-ruiz/elkbledom/blob/main/custom_components/elkbledom/elkbledom.py
"""

from typing import (
    Any,
    List,
)
from .consts import COMMAND_PREFIX

class BaseController:
    """
    base controller class
    """
    _char_specifier = None

    @property
    def char_specifier(self) -> str:
        """
        char specifier
        """
        assert self._char_specifier
        return self._char_specifier

    def __getattribute__(self, name: str) -> Any:
        if not name.startswith(COMMAND_PREFIX):
            return super().__getattribute__(name)
        act = name.removeprefix(COMMAND_PREFIX)
        command_fn = getattr(self, f"_{act}", None)
        if command_fn:
            return command_fn
        def command_wrapper():
            return getattr(self, f"_{COMMAND_PREFIX}{act}")
        return command_wrapper

class MELKController(BaseController):  # pylint: disable=R0903
    """
    MELK controller devices

    Implements:

    - BTLedStrip.exec_turn_on()
    - BTLedStrip.exec_turn_off()
    - BTLedStrip.exec_brightness(percentage: int)
    - BTLedStrip.exec_color(red: int, green: int, blue: int)
    """
    _char_specifier = "0000fff3-0000-1000-8000-00805f9b34fb"
    _command_turn_on = [0x7e, 0x00, 0x04, 0x01, 0x00, 0x00, 0x00, 0x00, 0xef]
    _command_turn_off = [0x7e, 0x00, 0x04, 0x00, 0x00, 0x00, 0xff, 0x00, 0xef]

    def _brightness(self, percentage: int = 0) -> List[bytes]:
        """
        set brightness
        """
        b = int(percentage * 255 / 100)
        return [0x7e, 0x04, 0x01, b, 0xff, 0x00, 0xff, 0x00, 0xef]

    def _color(self, red: int = 0, green: int = 0, blue: int = 0) -> List[bytes]:
        """
        set color
        """
        r = int(red * 255 / 100)
        g = int(green * 255 / 100)
        b = int(blue * 255 / 100)
        return [0x7e, 0x00, 0x05, 0x03, r, g, b, 0x00, 0xef]
