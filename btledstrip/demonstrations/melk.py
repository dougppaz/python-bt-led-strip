import argparse
import asyncio
import time
from btledstrip import (
    BTLedStrip,
    MELKController,
)

async def main(mac_address: str = None) -> None:
    assert mac_address
    controller = MELKController()
    async with BTLedStrip(controller, mac_address) as led_strip:
        while True:
            await led_strip.exec_color(red=100, green=100, blue=100)
            await led_strip.exec_brightness(percentage=100)
            await led_strip.exec_turn_on()
            time.sleep(1)
            await led_strip.exec_color(red=100, green=0, blue=0)
            time.sleep(1)
            await led_strip.exec_color(red=0, green=100, blue=0)
            time.sleep(1)
            await led_strip.exec_color(red=0, green=0, blue=100)
            time.sleep(1)
            brightness = 0
            await led_strip.exec_brightness(percentage=brightness)
            while brightness <= 100:
                await led_strip.exec_brightness(percentage=brightness)
                brightness += 1
            time.sleep(1)
            await led_strip.exec_brightness(percentage=0)
            await led_strip.exec_turn_off()
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='MELK Example')
    parser.add_argument('mac_address')
    args = parser.parse_args()
    asyncio.run(main(mac_address=args.mac_address))
