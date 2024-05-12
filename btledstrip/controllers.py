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
    Optional,
)
import datetime
from .typing import Command

COMMAND_PREFIX = "command_"

class Controller:
    """
    base controller class
    """
    _char_specifier: Optional[str] = None

    @property
    def char_specifier(self) -> str:
        """
        char specifier
        """
        assert self._char_specifier
        return self._char_specifier

    def init_commands(self) -> List[Command]:
        """
        init commands
        """
        return []

    def build_command(self, *args: int) -> Command:
        """
        build generic command
        """
        raise NotImplementedError()

    def __getattr__(self, name: str) -> Any:
        if not name.startswith(COMMAND_PREFIX):
            return super().__getattr__(name)
        act = name.removeprefix(COMMAND_PREFIX)
        command_fn = getattr(self, f"_{act}", None)
        if command_fn:
            return command_fn
        def command_wrapper():
            return getattr(self, f"_{COMMAND_PREFIX}{act}")
        return command_wrapper

class MELKController(Controller):  # pylint: disable=R0903
    """
    MELK controller devices

    Implements:

    - BTLedStrip.exec.turn_on()
    - BTLedStrip.exec.turn_off()
    - BTLedStrip.exec.brightness(percentage: int)
    - BTLedStrip.exec.color(red: float, green: float, blue: float)
    - BTLedStrip.exec.white(cold: int)
    - BTLedStrip.exec.white_cold(brightness: int)
    - BTLedStrip.exec.effect(number: int)
    - BTLedStrip.exec.effect_speed(velocity: int)
    """
    _char_specifier = "0000fff3-0000-1000-8000-00805f9b34fb"
    _command_turn_on: Command = [0x7e, 0x00, 0x04, 0x01, 0x00, 0x00, 0x00, 0x00, 0xef]
    _command_turn_off: Command = [0x7e, 0x00, 0x04, 0x00, 0x00, 0x00, 0xff, 0x00, 0xef]

    def init_commands(self) -> List[Command]:
        date = datetime.date.today()
        now = datetime.datetime.now()
        _, _, day_of_week = date.isocalendar()
        return [[0x7e, 0x07, 0x83],
                [0x7e, 0x04, 0x04],
                [0x7e, 0x00, 0x83, int(now.strftime('%H')), int(now.strftime('%M')),
                 int(now.strftime('%S')), day_of_week, 0x00, 0xef]]

    def build_command(self,  # pylint: disable=W0221,R0913
                      arg_1: int,
                      arg_2: int,
                      arg_3: int,
                      arg_4: int,
                      arg_5: int,
                      arg_6: int) -> Command:
        return [0x7e, arg_1, arg_2, arg_3, arg_4, arg_5, arg_6, 0x00, 0xef]

    def _brightness(self, percentage: int = 0) -> Command:
        """
        set brightness on color mode
        """
        return [0x7e, 0x04, 0x01, percentage, 0x00, 0x00, 0x00, 0x00, 0xef]

    def _color(self, red: float = 0, green: float = 0, blue: float = 0) -> Command:
        """
        mode color
        """
        r = int(red * 255 / 100)
        g = int(green * 255 / 100)
        b = int(blue * 255 / 100)
        return [0x7e, 0x00, 0x05, 0x03, r, g, b, 0x00, 0xef]

    def _white(self, cold: int = 0) -> Command:
        """
        mode white with temperature
        """
        return [0x7e, 0x00, 0x05, 0x02, 0x00, cold, 0x00, 0xef]

    def _white_cold(self, brightness: int = 0) -> Command:
        """
        mode white cold with brightness
        """
        return [0x7e, 0x00, 0x05, 0x01, brightness, 0x00, 0x00, 0xef]

    def _effect(self, number: int) -> Command:
        """
        mode effect
        """
        return [0x7e, 0x04, 0x03, number, 0x00, 0x00, 0x00, 0x00, 0xef]

    def _effect_speed(self, velocity: int = 0):
        """
        set effect speed
        """
        v = int(velocity)
        return [0x7e, 0x04, 0x02, v, 0x00, 0x00, 0x00, 0x00, 0xef]
