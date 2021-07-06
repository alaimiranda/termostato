#!/usr/bin/env python

import glob
import time

from gpiozero import LED

# Que devuelve w1_slave
# c3 00 4b 46 7f ff 0c 10 d6 : crc=41 YES
# c3 00 4b 46 7f ff 0c 10 d6 t=23187

ledverde = LED(22)
ledrojo = LED(23)

ledverde.on()
ledrojo.on()

while True:

   for sensor in glob.glob("/sys/bus/w1/devices/28-0*/w1_slave"):
      id = sensor.split("/")[5]

      try:
         f = open(sensor, "r")
         data = f.read()
         f.close()
         if "YES" in data:
            (discard, sep, reading) = data.partition(' t=')
            t = float(reading) / 1000.0
            print("{} {:.1f}".format(id, t))
            if t < 20:
                ledverde.on()
                ledrojo.off()
            else:
                ledverde.off()
                ledrojo.on()
         else:
            print("999.9")

      except:
         pass

   time.sleep(3.0)
