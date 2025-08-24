import network
import socket

# --- Wi-Fi Setup ---
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='lights domain', password='bloodforthebloodgod', authmode=network.AUTH_WPA2_PSK)
print("AP Active")
print("IP:", ap.ifconfig()[0])

# --- Game variable ---
counter = 0

# --- HTTP Server ---
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)
print("Listening on", addr)

while True:
    cl, addr = s.accept()
    request = cl.recv(1024)
    request = str(request)
    
    # Check if client pressed the increment button
    if "/increment" in request:
        counter += 1
    
    # Serve HTML page
    response = f"""\
HTTP/1.1 200 OK

<html>
    <head><title>Menu</title></head>
    <body>
        <h1>Shared Counter</h1>
        <p>Current Value: {counter}</p>
        <form action="/increment">
            <button type="submit">Increment</button>
        </form>
    </body>
</html>
"""
    cl.send(response)
    cl.close()
