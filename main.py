import psutil
import serial
import time
import logging

PORT = 'COM7'
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2) 

logging.basicConfig(
    filename='app.log',
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# sends command to esp8266
def send_command(cmd):
    logging.info(f"{bat[0]}% status : {"charging" if bat[1] else "not charging"}")
    ser.write((cmd + '\n').encode())
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    print("ESP:", response)
    logging.info(f"{bat[0]}% status : {"charging" if bat[1] else "not charging"}")


# returns [10, True]
def get_battery_percent():
    battery = psutil.sensors_battery()
    return [battery.percent,battery.power_plugged]

if __name__ == '__main__':
    while True:
        bat = get_battery_percent()
        if bat[0]>90 and bat[1]:
            send_command("off")
        elif bat[0]<20 and bat[1] == False:
            send_command("on")
        time.sleep(1)
