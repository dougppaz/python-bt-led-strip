"""
melk demonstration
"""
import logging
import argparse
import asyncio
from btledstrip import (
    BTLedStrip,
    MELKController,
)

async def main(mac_address: str) -> None:
    """
    run demonstration
    """
    controller = MELKController()
    async with BTLedStrip(controller, mac_address) as led_strip:
        await led_strip.exec.turn_on()
        while True:
            await led_strip.exec.brightness(percentage=100)
            await led_strip.exec.color(red=100)
            await asyncio.sleep(1)
            await led_strip.exec.color(green=100)
            await asyncio.sleep(1)
            await led_strip.exec.color(blue=100)
            await asyncio.sleep(1)
            p = 0
            await led_strip.exec.brightness(percentage=0)
            await led_strip.exec.color(green=100, blue=100)
            while p <= 100:
                await led_strip.exec.brightness(percentage=p)
                await asyncio.sleep(.05)
                p += 1
            await asyncio.sleep(1)
            await led_strip.exec.white()
            await asyncio.sleep(1)
            c = 0
            while c <= 100:
                await led_strip.exec.white(cold=c)
                await asyncio.sleep(.05)
                c += 1
            await asyncio.sleep(1)
            await led_strip.exec.white_cold(brightness=100)
            b = 100
            while b >= 0:
                await led_strip.exec.white_cold(brightness=b)
                await asyncio.sleep(.05)
                b -= 1
            await asyncio.sleep(1)
            await led_strip.exec.effect_speed(velocity=50)
            n = 0
            while n <= 255:
                await led_strip.exec.effect(number=n)
                await asyncio.sleep(1)
                n += 1

parser = argparse.ArgumentParser(prog='btledstrip MELK Demonstration')
parser.add_argument('mac_address')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    asyncio.run(main(mac_address=args.mac_address))
