import network
import socket
from time import sleep
import machine

# Yes, these could be in another file. But on the Pico! So no more secure. :)
SSID = "U+Net454C"
PASSWORD = "DDAE014478"

def move_forward():
    print ("Forward")
    
def move_backward():
    print ("Backward")
    
def move_stop():
    print ("Stop")
    
def move_left():
    print ("Left")
    
def move_right():
    print ("Right")
    
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Zumo Robot Control</title>
            </head>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Forward" style="height:300px; width:300px; font-size:30px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:300px; width:300px; font-size:30px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:300px; width:300px; font-size:30px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:300px; width:300px; font-size:30px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="Back" style="height:300px; width:300px; font-size:30px" />
            </form>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/forward?':
            move_forward()
        elif request =='/left?':
            move_left()
        elif request =='/stop?':
            move_stop()
        elif request =='/right?':
            move_right()
        elif request =='/back?':
            move_backward()
        html = webpage()
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
