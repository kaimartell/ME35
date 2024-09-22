import network
import time
import ubinascii

station = network.WLAN(network.STA_IF)
station.active(True)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

def scan_wifi():
    print("Scanning...")
    for _ in range(2):
        scan_result = station.scan()
        for ap in scan_result:
            print("SSID:%s BSSID:%s Channel:%d Strength:%d RSSI:%d Auth:%d "%(ap))
        print()
        time.sleep_ms(1000)
        
    #ask for input which wifi to connect to
    ssid = input("Enter the SSID of the wifi you want to connect to: ")
    password = input("Enter the password of the wifi you want to connect to: ")
    connect_to_wifi(ssid, password)

    
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while wlan.ifconfig()[0] == '0.0.0.0':
        print('connecting to network...')
        time.sleep(1)
        
    print('network config:', wlan.ifconfig())


def disconnect_from_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    print('disconnected from wifi')
    