```python
from btledstrip import (
    BTLedStrip,
    MELKController,
)

mac_address = "00:00:00:00:00:00"
controller = MELKController()
led_strip = BTLedStrip(controller, mac_address)

# turn on
await led_strip.exec_turn_on()

# turn off
await led_strip.exec_turn_off()
```
