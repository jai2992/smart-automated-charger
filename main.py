import psutil
import serial
import time
import logging
import serial.tools.list_ports
import threading
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image

ICON_PATH = "smart_charger.png"

logging.basicConfig(
    filename='app.log',
    filemode='a',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# find the port of esp8266 dynamically
def find_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "CH340" in port.description:
            return port.device
    return None

# connect the esp8266 to the device 
PORT = find_port()
BAUD = 9600
if PORT:
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2) 
        print("connected to PORT device",PORT)
        logging.info(f"device connected sucessfully through port {PORT}")
    except serial.SerialException as e:
        print("error in connecting device")
        ser = None
else:
    print("device not found connect device")
    logging.error("device not found")
    exit(1)


# sends command to esp8266
def send_command(cmd,bat):
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


def exit_app(icon, item):
    icon.stop()
    sys.exit()

def setup_tray_icon():
    image = Image.open(ICON_PATH)
    menu = Menu(MenuItem('Exit', exit_app))
    icon = Icon("BatteryMonitor", image, "Battery Monitor", menu)
    return icon

def monitor():
    while True:
        bat = get_battery_percent()
        if bat[0]>90 and bat[1]:
            send_command("off",bat)
        elif bat[0]<20 and bat[1] == False:
            send_command("on",bat)
        time.sleep(1)
if __name__ == '__main__':
    t = threading.Thread(target=monitor, daemon=True)
    t.start()

    tray_icon = setup_tray_icon()
    tray_icon.run()
    

