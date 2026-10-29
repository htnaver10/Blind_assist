from gpiozero import DistanceSensor, OutputDevice
import subprocess
import time

#Setup: tell the Pi which pins used
sensor = DistanceSensor(echo=24, trigger=23, max_distance=2)
motor = OutputDevice(18)

#Changeable settings
DETECT_RANGE_CM = 150
VOICE_RANGE_CM = 50
last_spoken_time = 0

print("BlindAssist running. Press Ctrl+C to stop.")

while True:
    distance_cm = sensor.distance * 100

    if distance_cm < DETECT_RANGE_CM:
        motor.on()
        time.sleep(0.08)
        motor.off()

        wait_time = distance_cm / 150
        if wait_time < 0.05:
            wait_time = 0.05
        time.sleep(wait_time)

        now = time.time()
        if distance_cm < VOICE_RANGE_CM and now - last_spoken_time > 3:
            subprocess.Popen(["espeak-ng", "Obstacle ahead"])
            last_spoken_time = now
    else:
        time.sleep(0.1)